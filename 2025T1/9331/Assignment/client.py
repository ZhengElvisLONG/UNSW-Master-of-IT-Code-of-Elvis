import socket
import threading
import json
import os
import sys
import time
import random
import struct

class ReliableUDP:
    """Implements reliable UDP communication with sequence numbers and acknowledgments"""
    
    def __init__(self, socket, timeout=0.5, max_retries=10):  # Increased max_retries from 5 to 10
        self.socket = socket
        self.timeout = timeout
        self.max_retries = max_retries
        self.sequence_number = random.randint(0, 65535)  # Random initial sequence number
        self.recv_buffer = {}  # Buffer for out-of-order packets
        self.ack_lock = threading.Lock()
        self.ack_received = {}  # Track received acknowledgments
        self.debug = True  # Enable debug messages for better diagnostics
    
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
    
    def send_reliable(self, message, address, custom_timeout=None, custom_retries=None):
        """Send a message reliably with retransmission"""
        # Use custom parameters if provided, otherwise use defaults
        timeout = custom_timeout if custom_timeout is not None else self.timeout
        max_retries = custom_retries if custom_retries is not None else self.max_retries
        
        seq_num = self.sequence_number
        self.sequence_number = (self.sequence_number + 1) % 65536
        
        packet = self._create_packet(message, seq_num)
        
        # Set up acknowledgment tracking
        with self.ack_lock:
            self.ack_received[seq_num] = False
        
        # Send with retransmission
        retries = 0
        while retries < max_retries:
            try:
                self._debug_print(f"Sending packet with seq_num {seq_num} to {address} (retry {retries+1}/{max_retries})")
                self.socket.sendto(packet, address)
                
                # Wait for acknowledgment
                start_time = time.time()
                while time.time() - start_time < timeout:
                    with self.ack_lock:
                        if self.ack_received.get(seq_num, False):
                            self._debug_print(f"Received ACK for seq_num {seq_num}")
                            # Clean up
                            self.ack_received.pop(seq_num, None)
                            return True
                    time.sleep(0.01)  # Small sleep to prevent CPU spinning
                
                self._debug_print(f"Timeout waiting for ACK for seq_num {seq_num}, retrying...")
                retries += 1
                # Exponential backoff for retries
                timeout = min(timeout * 1.5, 5.0)  # Increase timeout but cap at 5 seconds
            except Exception as e:
                self._debug_print(f"Error sending packet: {e}")
                retries += 1
        
        self._debug_print(f"Failed to send packet after {max_retries} retries")
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

class ForumClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.server_address = (server_host, server_port)
        self.udp_socket = None
        self.reliable_udp = None
        self.username = None
        self.stop_event = threading.Event()
        self.response_event = threading.Event()
        self.response_message = None
        self.response_lock = threading.Lock()
        self.download_dir = "downloads"
        
        # Create download directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
    
    def start(self):
        """Start the client and connect to server"""
        try:
            # Create UDP socket
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Initialize reliable UDP with increased timeout and retries for better reliability
            self.reliable_udp = ReliableUDP(self.udp_socket, timeout=2.0, max_retries=10)
            
            # Start response handler thread
            response_thread = threading.Thread(target=self.handle_responses)
            response_thread.daemon = True
            response_thread.start()
            
            # Main client loop
            self.client_loop()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if self.udp_socket:
                self.udp_socket.close()
    
    def handle_responses(self):
        """Handle server responses in a separate thread"""
        while not self.stop_event.is_set():
            try:
                message, address = self.reliable_udp.receive_reliable(timeout=0.5)
                if message and address == self.server_address:
                    with self.response_lock:
                        self.response_message = message
                        self.response_event.set()
            except Exception as e:
                print(f"Error handling response: {e}")
                time.sleep(0.1)  # Prevent CPU spinning
    
    def send_command(self, command, timeout=10.0, retries=15):
        """Send command to server and wait for response with custom timeout and retries"""
        try:
            # Clear previous response
            self.response_event.clear()
            
            # Send command with increased timeout and retries for critical operations
            if not self.reliable_udp.send_reliable(command, self.server_address, 
                                                  custom_timeout=2.0, custom_retries=retries):
                print("Failed to send command to server")
                return None
            
            # Wait for response with timeout
            if self.response_event.wait(timeout=timeout):
                with self.response_lock:
                    response = self.response_message
                    self.response_message = None
                    return response
            else:
                print("Timeout waiting for server response")
                return None
        except Exception as e:
            print(f"Error sending command: {e}")
            return None
    
    def authenticate(self, username, password):
        """Authenticate with the server with increased reliability"""
        # Use longer timeout and more retries for authentication
        command = f"AUTH {username} {password}"
        
        # Try authentication multiple times with increasing timeouts
        for attempt in range(3):
            print(f"Authentication attempt {attempt+1}/3...")
            response = self.send_command(command, timeout=15.0, retries=20)
            
            if response:
                if "successful login" in response or "created" in response:
                    self.username = username
                    return True
                elif "has logged in already" in response:
                    print("User is already logged in. Please try a different username.")
                    return False
            
            # Wait before retrying
            if attempt < 2:  # Don't wait after the last attempt
                print("Authentication failed, retrying...")
                time.sleep(2)
        
        return False
    
    def create_thread(self, thread_id):
        """Create a new thread"""
        command = f"CRT {thread_id}"
        response = self.send_command(command)
        print(response)
        return response
    
    def list_threads(self):
        """List all threads"""
        command = "LST"
        response = self.send_command(command)
        print(response)
        return response
    
    def post_message(self, thread_id, message):
        """Post a message to a thread"""
        command = f"MSG {thread_id} {message}"
        response = self.send_command(command)
        print(response)
        return response
    
    def delete_message(self, thread_id, message_id):
        """Delete a message"""
        command = f"DLT {thread_id} {message_id}"
        response = self.send_command(command)
        print(response)
        return response
    
    def edit_message(self, thread_id, message_id, new_content):
        """Edit a message"""
        command = f"EDT {thread_id} {message_id} {new_content}"
        response = self.send_command(command)
        print(response)
        return response
    
    def read_thread(self, thread_id):
        """Read a thread"""
        command = f"RDT {thread_id}"
        response = self.send_command(command)
        print(response)
        return response
    
    def upload_file(self, thread_id, file_path):
        """Upload a file to a thread"""
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist")
            return False
        
        filename = os.path.basename(file_path)
        
        # Send upload request via UDP with increased reliability
        command = f"UPD {thread_id} {filename}"
        response = self.send_command(command, timeout=15.0, retries=15)
        
        if not response or "Ready to receive" not in response:
            print(f"Upload request failed: {response}")
            return False
        
        print(f"Server response: {response}")
        
        # Extract port from response
        try:
            port = int(response.split("TCP port ")[1].strip())
        except (IndexError, ValueError):
            port = self.server_port  # Default to server port if parsing fails
        
        # Create TCP socket for file transfer
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server with timeout
            tcp_socket.settimeout(30.0)
            tcp_socket.connect((self.server_host, port))
            
            # Prepare metadata
            metadata = {
                'operation': 'upload',
                'username': self.username,
                'thread_id': thread_id,
                'filename': filename
            }
            
            # Send metadata with proper delimiter
            tcp_socket.sendall(json.dumps(metadata).encode('utf-8') + b'\n\n')
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Send file data in chunks with progress reporting
            with open(file_path, 'rb') as f:
                sent_bytes = 0
                start_time = time.time()
                
                # Use smaller chunk size for more frequent updates
                chunk_size = 64 * 1024  # 64KB chunks
                
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    
                    # Set longer timeout for data transfer
                    tcp_socket.settimeout(300.0)
                    tcp_socket.sendall(chunk)
                    
                    sent_bytes += len(chunk)
                    progress = (sent_bytes / file_size) * 100
                    
                    # Update progress every 10%
                    if int(progress) % 10 == 0:
                        elapsed = time.time() - start_time
                        speed = sent_bytes / (elapsed * 1024) if elapsed > 0 else 0
                        print(f"Upload progress: {progress:.1f}% ({sent_bytes}/{file_size} bytes) Speed: {speed:.2f} KB/s")
            
            # Signal end of file
            tcp_socket.shutdown(socket.SHUT_WR)
            
            # Wait for confirmation
            tcp_socket.settimeout(60.0)
            confirmation = tcp_socket.recv(4096).decode('utf-8')
            print(f"Upload confirmation: {confirmation}")
            
            if "UPLOAD_SUCCESS" in confirmation:
                print(f"File {filename} uploaded successfully")
                return True
            else:
                print(f"Upload failed: {confirmation}")
                return False
            
        except socket.timeout:
            print("Connection or transfer timed out")
            return False
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False
        finally:
            tcp_socket.close()
    
    def download_file(self, thread_id, filename):
        """Download a file from a thread"""
        # Send download request via UDP with increased reliability
        command = f"DWN {thread_id} {filename}"
        response = self.send_command(command, timeout=15.0, retries=15)
        
        if not response or "Ready to send" not in response:
            print(f"Download request failed: {response}")
            return False
        
        print(f"Server response: {response}")
        
        # Extract port from response
        try:
            port = int(response.split("TCP port ")[1].strip())
        except (IndexError, ValueError):
            port = self.server_port  # Default to server port if parsing fails
        
        # Create TCP socket for file transfer
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server with timeout
            tcp_socket.settimeout(30.0)
            tcp_socket.connect((self.server_host, port))
            
            # Prepare metadata
            metadata = {
                'operation': 'download',
                'username': self.username,
                'thread_id': thread_id,
                'filename': filename
            }
            
            # Send metadata with proper delimiter
            tcp_socket.sendall(json.dumps(metadata).encode('utf-8') + b'\n\n')
            
            # Prepare file path
            file_path = os.path.join(self.download_dir, filename)
            
            # Set longer timeout for data transfer
            tcp_socket.settimeout(300.0)
            
            # Wait for initial response
            initial_response = b''
            while b'\n' not in initial_response and len(initial_response) < 1024:
                chunk = tcp_socket.recv(1024)
                if not chunk:
                    break
                initial_response += chunk
            
            if b'FILE_TRANSFER_START' in initial_response:
                # Extract any file data that came with the header
                if b'\n' in initial_response:
                    header, file_data = initial_response.split(b'\n', 1)
                else:
                    file_data = b''
                
                # Receive file data with progress reporting
                received_bytes = len(file_data)
                start_time = time.time()
                
                with open(file_path, 'wb') as f:
                    # Write any data already received after the header
                    if file_data:
                        f.write(file_data)
                    
                    # Use smaller chunk size for more frequent updates
                    chunk_size = 64 * 1024  # 64KB chunks
                    
                    last_progress_report = 0
                    
                    while True:
                        try:
                            chunk = tcp_socket.recv(chunk_size)
                            if not chunk:
                                break
                            
                            f.write(chunk)
                            received_bytes += len(chunk)
                            
                            # Update progress every 256KB
                            if received_bytes - last_progress_report >= 256 * 1024:
                                elapsed = time.time() - start_time
                                speed = received_bytes / (elapsed * 1024) if elapsed > 0 else 0
                                print(f"Download progress: {received_bytes} bytes received. Speed: {speed:.2f} KB/s")
                                last_progress_report = received_bytes
                                
                        except socket.timeout:
                            print("Download timed out")
                            return False
                
                print(f"File {filename} downloaded successfully to {file_path}")
                print(f"Total received: {received_bytes} bytes")
                return True
            else:
                error_msg = initial_response.decode('utf-8', errors='replace')
                print(f"Download failed: {error_msg}")
                return False
            
        except socket.timeout:
            print("Connection or transfer timed out")
            return False
        except Exception as e:
            print(f"Error downloading file: {e}")
            return False
        finally:
            tcp_socket.close()
    
    def remove_thread(self, thread_id):
        """Remove a thread"""
        command = f"RMV {thread_id}"
        response = self.send_command(command)
        print(response)
        return response
    
    def exit(self):
        """Exit the client"""
        command = "XIT"
        response = self.send_command(command)
        print(response)
        self.stop_event.set()
        return response
    
    def client_loop(self):
        """Main client loop for user interaction"""
        print("Welcome to the Discussion Forum Client")
        print("Please login or create a new account")
        
        # Login loop
        while not self.stop_event.is_set():
            username = input("Username: ")
            password = input("Password: ")
            
            if self.authenticate(username, password):
                print(f"Welcome, {username}!")
                break
            else:
                print("Authentication failed. Please try again.")
        
        # Command loop
        while not self.stop_event.is_set():
            try:
                command_line = input("\nEnter command: ")
                parts = command_line.split()
                
                if not parts:
                    continue
                
                command = parts[0].upper()
                
                if command == "CRT":
                    if len(parts) >= 2:
                        thread_id = parts[1]
                        self.create_thread(thread_id)
                    else:
                        print("Usage: CRT <thread_id>")
                
                elif command == "LST":
                    self.list_threads()
                
                elif command == "MSG":
                    if len(parts) >= 3:
                        thread_id = parts[1]
                        message = ' '.join(parts[2:])
                        self.post_message(thread_id, message)
                    else:
                        print("Usage: MSG <thread_id> <message>")
                
                elif command == "DLT":
                    if len(parts) >= 3:
                        thread_id = parts[1]
                        message_id = parts[2]
                        self.delete_message(thread_id, message_id)
                    else:
                        print("Usage: DLT <thread_id> <message_id>")
                
                elif command == "EDT":
                    if len(parts) >= 4:
                        thread_id = parts[1]
                        message_id = parts[2]
                        new_content = ' '.join(parts[3:])
                        self.edit_message(thread_id, message_id, new_content)
                    else:
                        print("Usage: EDT <thread_id> <message_id> <message>")
                
                elif command == "RDT":
                    if len(parts) >= 2:
                        thread_id = parts[1]
                        self.read_thread(thread_id)
                    else:
                        print("Usage: RDT <thread_id>")
                
                elif command == "UPD":
                    if len(parts) >= 3:
                        thread_id = parts[1]
                        file_path = parts[2]
                        self.upload_file(thread_id, file_path)
                    else:
                        print("Usage: UPD <thread_id> <file_path>")
                
                elif command == "DWN":
                    if len(parts) >= 3:
                        thread_id = parts[1]
                        filename = parts[2]
                        self.download_file(thread_id, filename)
                    else:
                        print("Usage: DWN <thread_id> <filename>")
                
                elif command == "RMV":
                    if len(parts) >= 2:
                        thread_id = parts[1]
                        self.remove_thread(thread_id)
                    else:
                        print("Usage: RMV <thread_id>")
                
                elif command == "XIT":
                    self.exit()
                    break
                
                else:
                    print("Unknown command. Available commands:")
                    print("CRT, LST, MSG, DLT, EDT, RDT, UPD, DWN, RMV, XIT")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                self.stop_event.set()
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py <server_port>")
        sys.exit(1)
        
    try:
        server_port = int(sys.argv[1])
        client = ForumClient("127.0.0.1", server_port)
        client.start()
    except ValueError:
        print("Port must be an integer")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
