import socket
import threading
import json
import os
import sys
import time
from datetime import datetime
import random
import struct

class ReliableUDP:
    """Implements reliable UDP communication with sequence numbers and acknowledgments"""
    
    def __init__(self, socket, timeout=0.5, max_retries=5):
        self.socket = socket
        self.timeout = timeout
        self.max_retries = max_retries
        self.sequence_number = random.randint(0, 65535)  # Random initial sequence number
        self.recv_buffer = {}  # Buffer for out-of-order packets
        self.ack_lock = threading.Lock()
        self.ack_received = {}  # Track received acknowledgments
        self.debug = False  # Set to True to enable debug messages
    
    def _debug_print(self, message):
        """Print debug messages if debug mode is enabled"""
        if self.debug:
            print(f"[DEBUG] {message}")
    
    def _create_packet(self, message, seq_num=None):
        """Create a packet with header containing sequence number"""
        if seq_num is None:
            seq_num = self.sequence_number
        
        # Header format: 4 bytes for sequence number
        header = struct.pack("!I", seq_num)
        return header + message.encode('utf-8')
    
    def _parse_packet(self, packet):
        """Parse a packet to extract header and message"""
        if len(packet) < 4:
            return None, None
        
        # Extract sequence number from header
        seq_num = struct.unpack("!I", packet[:4])[0]
        message = packet[4:].decode('utf-8')
        return seq_num, message
    
    def _create_ack(self, seq_num):
        """Create an acknowledgment packet"""
        # ACK format: 'ACK' followed by sequence number
        return f"ACK {seq_num}".encode('utf-8')
    
    def _is_ack(self, packet):
        """Check if a packet is an acknowledgment"""
        try:
            message = packet.decode('utf-8')
            return message.startswith("ACK ")
        except:
            return False
    
    def _get_ack_seq_num(self, packet):
        """Extract sequence number from an acknowledgment packet"""
        try:
            message = packet.decode('utf-8')
            if message.startswith("ACK "):
                return int(message.split()[1])
        except:
            pass
        return None
    
    def send_reliable(self, message, address):
        """Send a message reliably with retransmission"""
        seq_num = self.sequence_number
        self.sequence_number = (self.sequence_number + 1) % 65536
        
        packet = self._create_packet(message, seq_num)
        
        # Set up acknowledgment tracking
        with self.ack_lock:
            self.ack_received[seq_num] = False
        
        # Send with retransmission
        retries = 0
        while retries < self.max_retries:
            try:
                self._debug_print(f"Sending packet with seq_num {seq_num} to {address}")
                self.socket.sendto(packet, address)
                
                # Wait for acknowledgment
                start_time = time.time()
                while time.time() - start_time < self.timeout:
                    with self.ack_lock:
                        if self.ack_received.get(seq_num, False):
                            self._debug_print(f"Received ACK for seq_num {seq_num}")
                            # Clean up
                            self.ack_received.pop(seq_num, None)
                            return True
                    time.sleep(0.01)  # Small sleep to prevent CPU spinning
                
                self._debug_print(f"Timeout waiting for ACK for seq_num {seq_num}, retrying...")
                retries += 1
            except Exception as e:
                self._debug_print(f"Error sending packet: {e}")
                retries += 1
        
        self._debug_print(f"Failed to send packet after {self.max_retries} retries")
        # Clean up
        with self.ack_lock:
            self.ack_received.pop(seq_num, None)
        return False
    
    def receive_reliable(self, buffer_size=4096, timeout=None):
        """Receive a message reliably and send acknowledgment"""
        original_timeout = self.socket.gettimeout()
        try:
            if timeout is not None:
                self.socket.settimeout(timeout)
            
            packet, address = self.socket.recvfrom(buffer_size)
            
            # Check if it's an acknowledgment
            if self._is_ack(packet):
                ack_seq_num = self._get_ack_seq_num(packet)
                if ack_seq_num is not None:
                    with self.ack_lock:
                        self.ack_received[ack_seq_num] = True
                    self._debug_print(f"Received ACK for seq_num {ack_seq_num}")
                return None, None
            
            # Extract sequence number and message
            seq_num, message = self._parse_packet(packet)
            if seq_num is None:
                self._debug_print(f"Received invalid packet from {address}")
                return None, None
            
            self._debug_print(f"Received packet with seq_num {seq_num} from {address}")
            
            # Send acknowledgment
            ack_packet = self._create_ack(seq_num)
            self.socket.sendto(ack_packet, address)
            self._debug_print(f"Sent ACK for seq_num {seq_num} to {address}")
            
            return message, address
        except socket.timeout:
            return None, None
        except Exception as e:
            self._debug_print(f"Error receiving packet: {e}")
            return None, None
        finally:
            self.socket.settimeout(original_timeout)
    
    def process_incoming_packets(self, handler_func, stop_event=None):
        """Process incoming packets in a separate thread"""
        while stop_event is None or not stop_event.is_set():
            try:
                message, address = self.receive_reliable()
                if message and address:
                    # Handle the message in a separate thread
                    threading.Thread(target=handler_func, args=(message, address)).start()
            except Exception as e:
                self._debug_print(f"Error processing incoming packet: {e}")
                time.sleep(0.1)  # Prevent CPU spinning in case of repeated errors

class ForumServer:
    def __init__(self, port):
        self.port = port
        self.udp_socket = None
        self.tcp_socket = None
        self.reliable_udp = None
        self.stop_event = threading.Event()

        # Data structures
        self.users = {}  # username -> password
        self.active_users = {}  # username -> client_address
        self.threads = {}  # threadID -> thread info
        self.messages = {}  # threadID -> list of messages
        self.files = {}  # threadID -> list of files

        # Use RLock instead of Lock to allow reentrant locking
        self.users_lock = threading.RLock()
        self.threads_lock = threading.RLock()
        self.messages_lock = threading.RLock()
        self.files_lock = threading.RLock()
        self.active_users_lock = threading.RLock()  # Dedicated lock for active_users

        # Create upload directory if it doesn't exist
        self.upload_dir = "uploads"
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

        # Load credentials from file
        self.load_credentials()

    def load_credentials(self):
        """Load user credentials from credentials.txt file"""
        try:
            with open("credentials.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(maxsplit=1)
                        if len(parts) == 2:
                            username, password = parts
                            self.users[username] = password
            print(f"Loaded {len(self.users)} user credentials")
        except FileNotFoundError:
            print("Warning: credentials.txt file not found. Using default credentials.")
            # Add default credentials if file not found
            self.users = {"Yoda": "jedi*knight", "R2D2": "c3p0sucks"}

    def start(self):
        """Start the server and listen for incoming connections"""
        # Start UDP server
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(('0.0.0.0', self.port))
        
        # Initialize reliable UDP
        self.reliable_udp = ReliableUDP(self.udp_socket)

        # Start TCP server for file transfers
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.bind(('0.0.0.0', self.port))
        self.tcp_socket.listen(10)  # Increased backlog for concurrent connections

        print(f"Server started on port {self.port}")
        print("Waiting for clients")

        # Start TCP listener thread
        tcp_thread = threading.Thread(target=self.handle_tcp_connections)
        tcp_thread.daemon = True
        tcp_thread.start()

        # Start UDP packet processor
        udp_thread = threading.Thread(target=self.reliable_udp.process_incoming_packets, 
                                     args=(self.handle_client_request, self.stop_event))
        udp_thread.daemon = True
        udp_thread.start()

        # Main loop to keep server running
        try:
            while not self.stop_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            print("Server shutting down...")
            self.stop_event.set()
        finally:
            self.udp_socket.close()
            self.tcp_socket.close()

    def handle_tcp_connections(self):
        """Handle incoming TCP connections for file transfers"""
        while not self.stop_event.is_set():
            try:
                client_socket, client_address = self.tcp_socket.accept()
                tcp_handler = threading.Thread(target=self.handle_file_transfer,
                                              args=(client_socket, client_address))
                tcp_handler.daemon = True
                tcp_handler.start()
            except OSError as e:
                if self.stop_event.is_set():
                    break
                print(f"TCP accept error: {e}")
            except Exception as e:
                print(f"Unexpected error in TCP handler: {e}")

    def handle_file_transfer(self, client_socket, client_address):
        """Handle TCP file transfers for uploads and downloads"""
        try:
            # Set initial timeout for metadata
            client_socket.settimeout(30.0)  # Increased to 30s for robustness
            metadata_bytes = b''
            metadata_complete = False
            remaining_data = b''

            # Receive metadata (terminated by \n\n or \n)
            while not metadata_complete:
                try:
                    chunk = client_socket.recv(1024)
                    if not chunk:
                        print(f"[ERROR] Client {client_address} disconnected before metadata")
                        client_socket.sendall(b"CLIENT_DISCONNECTED")
                        return
                    metadata_bytes += chunk
                    # Check for both \n\n and \n formats for compatibility
                    if b'\n\n' in metadata_bytes:
                        metadata_bytes, remaining_data = metadata_bytes.split(b'\n\n', 1)
                        metadata_complete = True
                    elif b'\n' in metadata_bytes and not b'\n\n' in metadata_bytes:
                        # For backward compatibility with clients that only send \n
                        metadata_bytes, remaining_data = metadata_bytes.split(b'\n', 1)
                        metadata_complete = True
                except socket.timeout:
                    print(f"[TIMEOUT] Metadata reception timeout from {client_address}")
                    client_socket.sendall(b"METADATA_TIMEOUT")
                    return
                except socket.error as e:
                    print(f"[ERROR] Socket error during metadata reception: {e}")
                    client_socket.sendall(b"SOCKET_ERROR")
                    return

            # Parse metadata
            try:
                metadata = json.loads(metadata_bytes.decode('utf-8'))
                print(f"[DEBUG] Received metadata from {client_address}: {metadata}")
                required_fields = ['operation', 'username', 'thread_id', 'filename']
                if not all(field in metadata for field in required_fields):
                    missing = [f for f in required_fields if f not in metadata]
                    print(f"[ERROR] Missing fields: {missing}")
                    client_socket.sendall(f"MISSING_FIELDS:{','.join(missing)}".encode('utf-8'))
                    return
                operation = metadata['operation']
                username = metadata['username']
                thread_id = str(metadata['thread_id'])
                filename = metadata['filename']
                
                # Verify user is authenticated - use a short timeout for this check
                is_authenticated = False
                try:
                    with self.active_users_lock:
                        is_authenticated = username in self.active_users
                except Exception as e:
                    print(f"[ERROR] Authentication check error: {e}")
                
                if not is_authenticated:
                    print(f"[ERROR] User {username} not authenticated for file transfer")
                    client_socket.sendall(b"USER_NOT_AUTHENTICATED")
                    return
                
            except json.JSONDecodeError as e:
                print(f"[ERROR] Invalid JSON from {client_address}: {e}")
                client_socket.sendall(b"INVALID_JSON")
                return
            except UnicodeDecodeError as e:
                print(f"[ERROR] Encoding error from {client_address}: {e}")
                client_socket.sendall(b"ENCODING_ERROR")
                return

            # Handle upload
            if operation == 'upload':
                try:
                    # Verify thread exists - use a short lock
                    thread_exists = False
                    try:
                        with self.threads_lock:
                            thread_exists = thread_id in self.threads
                    except Exception as e:
                        print(f"[ERROR] Thread check error: {e}")
                        client_socket.sendall(b"THREAD_CHECK_ERROR")
                        return
                            
                    if not thread_exists:
                        print(f"[ERROR] Thread {thread_id} does not exist")
                        client_socket.sendall(b"THREAD_NOT_FOUND")
                        return
                    
                    # Use platform-independent path separator
                    file_path = os.path.join(self.upload_dir, f"{thread_id}_{filename}")
                    print(f"[UPLOAD] Receiving {filename} to {file_path}")
                    os.makedirs(self.upload_dir, exist_ok=True)
                    
                    # Increased timeout for file data - 5 minutes for large files
                    client_socket.settimeout(300.0)
                    received_bytes = 0
                    start_time = time.time()
                    last_activity_time = time.time()
                    
                    # File I/O operations outside of locks
                    with open(file_path, 'wb') as f:
                        if remaining_data:
                            f.write(remaining_data)
                            received_bytes += len(remaining_data)
                            last_activity_time = time.time()
                        
                        # Set a maximum inactivity period (2 minutes)
                        max_inactivity = 120.0
                        
                        while True:
                            try:
                                # Check for inactivity timeout
                                if time.time() - last_activity_time > max_inactivity:
                                    print(f"[TIMEOUT] Inactivity timeout from {client_address}")
                                    client_socket.sendall(b"INACTIVITY_TIMEOUT")
                                    return
                                
                                # Use smaller chunk size for more frequent updates
                                chunk = client_socket.recv(64 * 1024)  # 64KB chunks
                                
                                # If no data and we've received something, consider it complete
                                if not chunk:
                                    if received_bytes > 0:
                                        print(f"[INFO] Client finished sending data")
                                        break
                                    else:
                                        print(f"[ERROR] Client disconnected without sending data")
                                        client_socket.sendall(b"NO_DATA_RECEIVED")
                                        return
                                
                                f.write(chunk)
                                received_bytes += len(chunk)
                                last_activity_time = time.time()
                                
                                # More frequent progress updates
                                if received_bytes % (1024 * 1024) == 0:  # Every 1MB
                                    elapsed = time.time() - start_time
                                    speed = received_bytes / (elapsed * 1024) if elapsed > 0 else 0
                                    print(f"[STATUS] Received: {received_bytes/1024:.2f}KB Speed: {speed:.2f}KB/s")
                                    
                            except socket.timeout:
                                # If we've received data but timed out, consider it complete
                                if received_bytes > 0:
                                    print(f"[INFO] Upload timed out but data received, considering complete")
                                    break
                                else:
                                    print(f"[TIMEOUT] File transfer timeout from {client_address}")
                                    client_socket.sendall(b"TRANSFER_TIMEOUT")
                                    return
                            except socket.error as e:
                                print(f"[ERROR] Socket error during upload: {e}")
                                client_socket.sendall(b"TRANSFER_ERROR")
                                return
                    
                    # Update file metadata with a short lock
                    try:
                        with self.files_lock:
                            if thread_id not in self.files:
                                self.files[thread_id] = []
                            self.files[thread_id].append({
                                'filename': filename,
                                'uploader': username,
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'path': file_path,
                                'size': received_bytes
                            })
                    except Exception as e:
                        print(f"[ERROR] File metadata update error: {e}")
                        # Continue anyway, file is already saved
                    
                    print(f"[SUCCESS] Uploaded {filename} ({received_bytes} bytes)")
                    client_socket.sendall(b"UPLOAD_SUCCESS")
                    
                except PermissionError as e:
                    print(f"[ERROR] Permission denied for {file_path}: {e}")
                    client_socket.sendall(b"PERMISSION_DENIED")
                    return
                except Exception as e:
                    print(f"[ERROR] Upload error: {type(e).__name__}: {e}")
                    client_socket.sendall(f"UPLOAD_ERROR:{str(e)}".encode('utf-8'))
                    return

            # Handle download
            elif operation == 'download':
                try:
                    # Verify thread exists - use a short lock
                    thread_exists = False
                    try:
                        with self.threads_lock:
                            thread_exists = thread_id in self.threads
                    except Exception as e:
                        print(f"[ERROR] Thread check error: {e}")
                        client_socket.sendall(b"THREAD_CHECK_ERROR")
                        return
                            
                    if not thread_exists:
                        print(f"[ERROR] Thread {thread_id} does not exist")
                        client_socket.sendall(b"THREAD_NOT_FOUND")
                        return
                    
                    # Find file path - use a short lock
                    file_path = None
                    try:
                        with self.files_lock:
                            if thread_id in self.files:
                                for file_info in self.files[thread_id]:
                                    if file_info['filename'] == filename:
                                        file_path = file_info['path']
                                        break
                    except Exception as e:
                        print(f"[ERROR] File lookup error: {e}")
                        client_socket.sendall(b"FILE_LOOKUP_ERROR")
                        return
                    
                    if not file_path or not os.path.exists(file_path):
                        print(f"[ERROR] File {filename} not found for thread {thread_id}")
                        client_socket.sendall(b"FILE_NOT_FOUND")
                        return
                    
                    # Get file size outside of locks
                    try:
                        file_size = os.path.getsize(file_path)
                    except Exception as e:
                        print(f"[ERROR] File size check error: {e}")
                        client_socket.sendall(b"FILE_SIZE_ERROR")
                        return
                    
                    print(f"[DOWNLOAD] Sending {filename} ({file_size} bytes)")
                    
                    # Send file info - modified to match client expectation
                    client_socket.sendall(b"FILE_TRANSFER_START\n")
                    
                    # Increased timeout for file data
                    client_socket.settimeout(300.0)
                    sent_bytes = 0
                    start_time = time.time()
                    
                    # File I/O operations outside of locks
                    try:
                        with open(file_path, 'rb') as f:
                            while True:
                                # Use smaller chunk size for more frequent updates
                                chunk = f.read(64 * 1024)  # 64KB chunks
                                if not chunk:
                                    break
                                try:
                                    client_socket.sendall(chunk)
                                    sent_bytes += len(chunk)
                                    if sent_bytes % (1024 * 1024) == 0:  # Every 1MB
                                        elapsed = time.time() - start_time
                                        speed = sent_bytes / (elapsed * 1024) if elapsed > 0 else 0
                                        progress = (sent_bytes / file_size) * 100
                                        print(f"[STATUS] Sent: {progress:.1f}% Speed: {speed:.2f}KB/s")
                                except socket.error as e:
                                    print(f"[ERROR] Socket error during download: {e}")
                                    client_socket.sendall(b"TRANSFER_ERROR")
                                    return
                    except Exception as e:
                        print(f"[ERROR] File read error: {e}")
                        client_socket.sendall(b"FILE_READ_ERROR")
                        return
                    
                    print(f"[SUCCESS] Downloaded {filename} ({sent_bytes} bytes)")
                    
                except PermissionError as e:
                    print(f"[ERROR] Permission denied for {file_path}: {e}")
                    client_socket.sendall(b"READ_PERMISSION_DENIED")
                    return
                except Exception as e:
                    print(f"[ERROR] Download error: {type(e).__name__}: {e}")
                    client_socket.sendall(f"DOWNLOAD_ERROR:{str(e)}".encode('utf-8'))
                    return

            else:
                print(f"[ERROR] Invalid operation: {operation}")
                client_socket.sendall(b"INVALID_OPERATION")
                return

        except Exception as e:
            print(f"[CRITICAL] Fatal error in file transfer from {client_address}: {type(e).__name__}: {e}")
            try:
                client_socket.sendall(f"FATAL_ERROR:{str(e)}".encode('utf-8'))
            except:
                pass
        finally:
            try:
                client_socket.close()
                print(f"[DEBUG] TCP Connection closed for {client_address}")
            except:
                pass
    
    def is_user_authenticated(self, username):
        """Check if a user is authenticated"""
        try:
            with self.active_users_lock:
                return username in self.active_users
        except Exception as e:
            print(f"[ERROR] Authentication check error: {e}")
            return False
            
    def handle_client_request(self, message, client_address):
        """Handle client UDP requests"""
        try:
            parts = message.split()

            if not parts:
                return

            command = parts[0]

            # Handle authentication
            if command == "AUTH":
                if len(parts) >= 3:
                    username = parts[1]
                    password = parts[2]
                    self.handle_auth(username, password, client_address)
                else:
                    self.send_response("Invalid authentication format", client_address)

            # Handle other commands (require authentication check)
            else:
                # Find username by client address
                username = None
                try:
                    with self.active_users_lock:
                        for user, addr in self.active_users.items():
                            if addr == client_address:
                                username = user
                                break
                except Exception as e:
                    print(f"[ERROR] User lookup error: {e}")
                    self.send_response("Server error during authentication", client_address)
                    return

                if username is None:
                    self.send_response("Not logged in", client_address)
                    return

                if command == "CRT":  # Create thread
                    if len(parts) >= 2:
                        thread_id = parts[1]
                        self.handle_create_thread(username, thread_id, client_address)
                    else:
                        self.send_response("Invalid CRT format", client_address)

                elif command == "LST":  # List threads
                    self.handle_list_threads(username, client_address)

                elif command == "MSG":  # Post message
                    if len(parts) >= 3:
                        thread_id = parts[1]
                        message_content = ' '.join(parts[2:])
                        self.handle_post_message(username, thread_id, message_content, client_address)
                    else:
                        self.send_response("Invalid MSG format", client_address)

                elif command == "DLT":  # Delete message
                    if len(parts) >= 3:
                        thread_id = parts[1]
                        message_id = parts[2]
                        self.handle_delete_message(username, thread_id, message_id, client_address)
                    else:
                        self.send_response("Invalid DLT format", client_address)

                elif command == "EDT":  # Edit message
                    if len(parts) >= 4:
                        thread_id = parts[1]
                        message_id = parts[2]
                        new_content = ' '.join(parts[3:])
                        self.handle_edit_message(username, thread_id, message_id, new_content, client_address)
                    else:
                        self.send_response("Invalid EDT format", client_address)

                elif command == "RDT":  # Read thread
                    if len(parts) >= 2:
                        thread_id = parts[1]
                        self.handle_read_thread(username, thread_id, client_address)
                    else:
                        self.send_response("Invalid RDT format", client_address)

                elif command == "UPD":  # Upload file (UDP part)
                    if len(parts) >= 3:
                        thread_id = parts[1]
                        filename = parts[2]
                        self.handle_upload_request(username, thread_id, filename, client_address)
                    else:
                        self.send_response("Invalid UPD format", client_address)

                elif command == "DWN":  # Download file (UDP part)
                    if len(parts) >= 3:
                        thread_id = parts[1]
                        filename = parts[2]
                        self.handle_download_request(username, thread_id, filename, client_address)
                    else:
                        self.send_response("Invalid DWN format", client_address)

                elif command == "RMV":  # Remove thread
                    if len(parts) >= 2:
                        thread_id = parts[1]
                        self.handle_remove_thread(username, thread_id, client_address)
                    else:
                        self.send_response("Invalid RMV format", client_address)

                elif command == "XIT":  # Exit
                    self.handle_exit(username, client_address)

                else:
                    self.send_response("Unknown command", client_address)

        except Exception as e:
            print(f"Error handling client request: {e}")
            self.send_response(f"Server error: {str(e)}", client_address)

    def send_response(self, message, client_address):
        """Send UDP response to client using reliable UDP"""
        try:
            self.reliable_udp.send_reliable(message, client_address)
        except Exception as e:
            print(f"Error sending response to {client_address}: {e}")
        
    def handle_auth(self, username, password, client_address):
        """Handle user authentication"""
        print(f"Client authenticating")
        
        try:
            with self.active_users_lock:
                # Check if this client address is already logged in
                for user, addr in self.active_users.items():
                    if addr == client_address:
                        # If same user is trying to login again, allow it
                        if user == username:
                            self.send_response(f"{username} successful login\nWelcome to the forum", client_address)
                            print(f"{username} successful login")
                            return
                        # Otherwise, force logout of previous user
                        else:
                            del self.active_users[user]
                            break
                
                # Check if username is already logged in from another client
                if username in self.active_users:
                    self.send_response(f"{username} has logged in already", client_address)
                    print(f"{username} has logged in already")
                    return
                    
                # Validate credentials
                with self.users_lock:
                    if username in self.users and self.users[username] == password:
                        self.active_users[username] = client_address
                        self.send_response(f"{username} successful login\nWelcome to the forum", client_address)
                        print(f"{username} successful login")
                    else:
                        # Create new user if username doesn't exist
                        self.users[username] = password
                        
                        # Add to credentials file
                        try:
                            with open("credentials.txt", "a") as f:
                                f.write(f"\n{username} {password}")
                            print(f"New user {username} created")
                        except Exception as e:
                            print(f"Error adding user to credentials file: {e}")
                        
                        # Add user to active users
                        self.active_users[username] = client_address
                        self.send_response(f"New user {username} created\nWelcome to the forum", client_address)
                        print(f"{username} logged in")
        except Exception as e:
            print(f"Error in authentication: {e}")
            self.send_response(f"Authentication error: {str(e)}", client_address)
                
    def handle_create_thread(self, username, thread_id, client_address):
        """Handle thread creation"""
        try:
            thread_exists = False
            with self.threads_lock:
                thread_exists = thread_id in self.threads
                
            if thread_exists:
                self.send_response(f"Thread {thread_id} exists", client_address)
                print(f"{username} issued command CRT\nThread {thread_id} exists")
                return
                
            # Create thread with minimal lock time
            with self.threads_lock:
                self.threads[thread_id] = {
                    'creator': username,
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            
            # Initialize empty message list with separate lock
            with self.messages_lock:
                self.messages[thread_id] = []
                
            # Initialize empty file list with separate lock
            with self.files_lock:
                self.files[thread_id] = []
                
            self.send_response(f"Thread {thread_id} created", client_address)
            print(f"{username} issued command CRT\nThread {thread_id} created")
        except Exception as e:
            print(f"Error creating thread: {e}")
            self.send_response(f"Error creating thread: {str(e)}", client_address)
            
    def handle_list_threads(self, username, client_address):
        """Handle thread listing"""
        print(f"{username} issued command LST")
        
        try:
            thread_list = []
            with self.threads_lock:
                if not self.threads:
                    self.send_response("No threads to list", client_address)
                    return
                    
                for thread_id, thread_info in self.threads.items():
                    thread_list.append(f"{thread_id}: {thread_info['creator']}")
                    
            self.send_response("\n".join(thread_list), client_address)
        except Exception as e:
            print(f"Error listing threads: {e}")
            self.send_response(f"Error listing threads: {str(e)}", client_address)
            
    def handle_post_message(self, username, thread_id, content, client_address):
        """Handle posting a message to a thread"""
        print(f"{username} issued command MSG")
        
        try:
            # Check if thread exists
            thread_exists = False
            with self.threads_lock:
                thread_exists = thread_id in self.threads
                
            if not thread_exists:
                self.send_response(f"Thread {thread_id} does not exist", client_address)
                return
                
            # Add message with minimal lock time
            with self.messages_lock:
                if thread_id not in self.messages:
                    self.messages[thread_id] = []
                    
                # Add message with ID (1-based indexing)
                message_id = len(self.messages[thread_id]) + 1
                self.messages[thread_id].append({
                    'id': message_id,
                    'author': username,
                    'content': content,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
            self.send_response(f"Message posted to {thread_id} thread", client_address)
            print(f"Message posted to {thread_id} thread")
        except Exception as e:
            print(f"Error posting message: {e}")
            self.send_response(f"Error posting message: {str(e)}", client_address)
                
    def handle_delete_message(self, username, thread_id, message_id, client_address):
        """Handle deleting a message"""
        try:
            message_id = int(message_id)
            print(f"{username} issued command DLT")
            
            # Check if thread exists
            thread_exists = False
            with self.threads_lock:
                thread_exists = thread_id in self.threads
                
            if not thread_exists:
                self.send_response(f"Thread {thread_id} does not exist", client_address)
                return
                
            # Check and delete message with minimal lock time
            with self.messages_lock:
                if thread_id not in self.messages:
                    self.send_response(f"Thread {thread_id} has no messages", client_address)
                    return
                    
                # Find the message by ID
                message_found = False
                message_author = None
                message_index = -1
                
                for i, message in enumerate(self.messages[thread_id]):
                    if message['id'] == message_id:
                        message_author = message['author']
                        message_index = i
                        message_found = True
                        break
                
                if not message_found:
                    self.send_response(f"Message {message_id} not found in thread {thread_id}", client_address)
                    return
                
                # Check if user is the author
                if message_author != username:
                    self.send_response("The message belongs to another user and cannot be deleted", client_address)
                    print("Message cannot be deleted")
                    return
                    
                # Delete the message
                del self.messages[thread_id][message_index]
                
                # Renumber remaining messages
                for i, message in enumerate(self.messages[thread_id]):
                    message['id'] = i + 1
                    
            self.send_response("The message has been deleted", client_address)
            print("Message has been deleted")
                        
        except ValueError:
            self.send_response("Invalid message ID format", client_address)
        except Exception as e:
            print(f"Error deleting message: {e}")
            self.send_response(f"Error deleting message: {str(e)}", client_address)
            
    def handle_edit_message(self, username, thread_id, message_id, new_content, client_address):
        """Handle editing a message"""
        try:
            message_id = int(message_id)
            print(f"{username} issued command EDT")
            
            # Check if thread exists
            thread_exists = False
            with self.threads_lock:
                thread_exists = thread_id in self.threads
                
            if not thread_exists:
                self.send_response(f"Thread {thread_id} does not exist", client_address)
                return
                
            # Check and edit message with minimal lock time
            with self.messages_lock:
                if thread_id not in self.messages:
                    self.send_response(f"Thread {thread_id} has no messages", client_address)
                    return
                    
                # Find the message by ID
                message_found = False
                for message in self.messages[thread_id]:
                    if message['id'] == message_id:
                        # Check if user is the author
                        if message['author'] != username:
                            self.send_response("The message belongs to another user and cannot be edited", client_address)
                            print("Message cannot be edited")
                            return
                            
                        # Edit the message
                        message['content'] = new_content
                        message['edited_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        message_found = True
                        break
                        
                if not message_found:
                    self.send_response(f"Message {message_id} not found in thread {thread_id}", client_address)
                    return
                    
            self.send_response("The message has been edited", client_address)
            print("Message has been edited")
                        
        except ValueError:
            self.send_response("Invalid message ID format", client_address)
        except Exception as e:
            print(f"Error editing message: {e}")
            self.send_response(f"Error editing message: {str(e)}", client_address)
            
    def handle_read_thread(self, username, thread_id, client_address):
        """Handle reading a thread"""
        print(f"{username} issued command RDT")
        
        try:
            # Check if thread exists
            thread_exists = False
            with self.threads_lock:
                thread_exists = thread_id in self.threads
                
            if not thread_exists:
                self.send_response(f"Thread {thread_id} does not exist", client_address)
                return
                
            # Get messages with minimal lock time
            message_lines = []
            with self.messages_lock:
                if thread_id not in self.messages or not self.messages[thread_id]:
                    self.send_response(f"Thread {thread_id} has no messages", client_address)
                    return
                    
                # Format messages
                for message in self.messages[thread_id]:
                    message_lines.append(f"{message['id']} {message['author']}: {message['content']}")
                    
            response = "\n".join(message_lines)
            self.send_response(response, client_address)
            print(f"Thread {thread_id} read")
                
            # Check if there are files in this thread - separate lock
            file_lines = []
            with self.files_lock:
                if thread_id in self.files and self.files[thread_id]:
                    for file_info in self.files[thread_id]:
                        file_lines.append(f"{file_info['uploader']} uploaded {file_info['filename']}")
                        
            if file_lines:
                file_response = "\n".join(file_lines)
                # Send a separate response for files
                time.sleep(0.1)  # Small delay to ensure messages arrive in order
                self.send_response(file_response, client_address)
        except Exception as e:
            print(f"Error reading thread: {e}")
            self.send_response(f"Error reading thread: {str(e)}", client_address)
                
    def handle_upload_request(self, username, thread_id, filename, client_address):
        """Handle file upload request (UDP part)"""
        print(f"{username} issued command UPD")
        
        try:
            # Check if thread exists
            thread_exists = False
            with self.threads_lock:
                thread_exists = thread_id in self.threads
                
            if not thread_exists:
                self.send_response(f"Thread {thread_id} does not exist", client_address)
                return
                
            # Send TCP port information for file transfer
            self.send_response(f"Ready to receive {filename} on TCP port {self.port}", client_address)
        except Exception as e:
            print(f"Error handling upload request: {e}")
            self.send_response(f"Error handling upload request: {str(e)}", client_address)
            
    def handle_download_request(self, username, thread_id, filename, client_address):
        """Handle file download request (UDP part)"""
        print(f"{username} issued command DWN")
        
        try:
            # Check if thread exists
            thread_exists = False
            with self.threads_lock:
                thread_exists = thread_id in self.threads
                
            if not thread_exists:
                self.send_response(f"Thread {thread_id} does not exist", client_address)
                return
                
            # Check if file exists with minimal lock time
            file_found = False
            with self.files_lock:
                if thread_id in self.files:
                    for file_info in self.files[thread_id]:
                        if file_info['filename'] == filename:
                            file_found = True
                            break
                            
            if not file_found:
                self.send_response(f"File {filename} not found in thread {thread_id}", client_address)
                return
                
            # Send TCP port information for file transfer
            self.send_response(f"Ready to send {filename} on TCP port {self.port}", client_address)
        except Exception as e:
            print(f"Error handling download request: {e}")
            self.send_response(f"Error handling download request: {str(e)}", client_address)
                
    def handle_remove_thread(self, username, thread_id, client_address):
        """Handle thread removal"""
        print(f"{username} issued command RMV")
        
        try:
            # Check if thread exists and user is creator
            thread_exists = False
            thread_creator = None
            
            with self.threads_lock:
                if thread_id in self.threads:
                    thread_exists = True
                    thread_creator = self.threads[thread_id]['creator']
                
            if not thread_exists:
                self.send_response(f"Thread {thread_id} does not exist", client_address)
                return
                
            # Check if user is the thread creator
            if thread_creator != username:
                self.send_response(f"Thread {thread_id} cannot be removed", client_address)
                print(f"Thread {thread_id} cannot be removed")
                return
                
            # Get file paths to delete before removing thread data
            file_paths = []
            with self.files_lock:
                if thread_id in self.files:
                    for file_info in self.files[thread_id]:
                        if os.path.exists(file_info['path']):
                            file_paths.append(file_info['path'])
            
            # Remove thread data with separate locks to minimize contention
            with self.threads_lock:
                if thread_id in self.threads:
                    del self.threads[thread_id]
                    
            with self.messages_lock:
                if thread_id in self.messages:
                    del self.messages[thread_id]
                    
            with self.files_lock:
                if thread_id in self.files:
                    del self.files[thread_id]
            
            # Delete physical files outside of locks
            for path in file_paths:
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"Error removing file {path}: {e}")
                    
            self.send_response(f"Thread {thread_id} removed", client_address)
            print(f"Thread {thread_id} removed")
        except Exception as e:
            print(f"Error removing thread: {e}")
            self.send_response(f"Error removing thread: {str(e)}", client_address)
            
    def handle_exit(self, username, client_address):
        """Handle client exit"""
        try:
            with self.active_users_lock:
                if username in self.active_users:
                    del self.active_users[username]
                    
            self.send_response("Goodbye", client_address)
            print(f"{username} exited")
        except Exception as e:
            print(f"Error handling exit: {e}")
            self.send_response(f"Error handling exit: {str(e)}", client_address)

def main():
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
        
    try:
        port = int(sys.argv[1])
        server = ForumServer(port)
        server.start()
    except ValueError:
        print("Port must be an integer")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
