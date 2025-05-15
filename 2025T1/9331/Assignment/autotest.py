#!/usr/bin/env python3
"""
COMP3331/9331 Computer Networks and Applications
Enhanced Comprehensive Autotest Script for Discussion Forum Application

This script provides a comprehensive testing framework for the discussion forum
application, capturing and displaying all server and client outputs.
"""
import subprocess
import time
import os
import signal
import threading
import shutil
import socket
import json
import sys
import queue
import random
import argparse
from datetime import datetime

class OutputCapture:
    """Captures and displays output from subprocesses in real-time"""
    
    def __init__(self, name, color_code=None):
        self.name = name
        self.color_code = color_code
        self.output_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.display_thread = None
    
    def start_capture(self):
        """Start the output display thread"""
        self.display_thread = threading.Thread(target=self._display_output)
        self.display_thread.daemon = True
        self.display_thread.start()
    
    def stop_capture(self):
        """Stop the output display thread"""
        if self.display_thread:
            self.stop_event.set()
            self.display_thread.join(timeout=2)
    
    def _display_output(self):
        """Display output from the queue"""
        while not self.stop_event.is_set():
            try:
                line = self.output_queue.get(timeout=0.1)
                if self.color_code:
                    print(f"{self.color_code}[{self.name}] {line}\033[0m")
                else:
                    print(f"[{self.name}] {line}")
                self.output_queue.task_done()
            except queue.Empty:
                continue
    
    def process_output(self, stream, prefix=""):
        """Process output from a stream and add to queue"""
        for line in iter(stream.readline, ''):
            if line:
                self.output_queue.put(f"{prefix}{line.rstrip()}")
                if self.stop_event.is_set():
                    break
    
    def add_output(self, line):
        """Add a line to the output queue"""
        self.output_queue.put(line)

class EnhancedAutoTest:
    """Enhanced automated testing framework for the discussion forum application"""
    
    # ANSI color codes for output
    COLORS = {
        'server': '\033[94m',  # Blue
        'client1': '\033[92m', # Green
        'client2': '\033[93m', # Yellow
        'client3': '\033[91m', # Red
        'client4': '\033[96m', # Cyan
        'client5': '\033[95m', # Magenta
        'test': '\033[95m',    # Magenta
        'error': '\033[91m',   # Red
        'success': '\033[92m', # Green
    }
    
    def __init__(self, server_script="server.py", client_script="client.py", port=6000):
        self.server_script = server_script
        self.client_script = client_script
        self.server_process = None
        self.client_processes = []
        self.port = port
        self.test_files_dir = "test_files"
        self.server_ip = "127.0.0.1"
        
        # Output capture objects
        self.server_output = OutputCapture("SERVER", self.COLORS['server'])
        self.client_outputs = {}
        self.test_output = OutputCapture("TEST", self.COLORS['test'])
        
        # Start output capture
        self.server_output.start_capture()
        self.test_output.start_capture()
        
        # Create test directories
        self._create_directories()
        
        # Create test files
        self.create_test_files()
        
        # Log test start
        self.log(f"Enhanced AutoTest started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Server script: {server_script}")
        self.log(f"Client script: {client_script}")
        self.log(f"Port: {port}")
    
    def _create_directories(self):
        """Create necessary directories for testing"""
        directories = [self.test_files_dir, "downloads", "uploads"]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                self.log(f"Created directory: {directory}")
    
    def log(self, message, level="info"):
        """Log a message to the test output"""
        if level == "error":
            self.test_output.add_output(f"{self.COLORS['error']}{message}\033[0m")
        elif level == "success":
            self.test_output.add_output(f"{self.COLORS['success']}{message}\033[0m")
        else:
            self.test_output.add_output(message)
    
    def create_test_files(self):
        """Create test files of various sizes for upload/download testing"""
        self.log("Creating test files...")
        
        # Small file (10KB)
        small_file = os.path.join(self.test_files_dir, "small.txt")
        with open(small_file, "w") as f:
            f.write("This is a small test file for upload testing.\n" * 100)
        self.log(f"Created small test file: {small_file} ({os.path.getsize(small_file)} bytes)")
        
        # Medium file (100KB)
        medium_file = os.path.join(self.test_files_dir, "medium.txt")
        with open(medium_file, "w") as f:
            f.write("This is a medium test file for upload testing.\n" * 1000)
        self.log(f"Created medium test file: {medium_file} ({os.path.getsize(medium_file)} bytes)")
        
        # Large file (1MB)
        large_file = os.path.join(self.test_files_dir, "large.txt")
        with open(large_file, "w") as f:
            f.write("This is a large test file for upload testing.\n" * 10000)
        self.log(f"Created large test file: {large_file} ({os.path.getsize(large_file)} bytes)")
        
        # Binary file
        binary_file = os.path.join(self.test_files_dir, "binary.dat")
        with open(binary_file, "wb") as f:
            f.write(os.urandom(50 * 1024))  # 50KB of random binary data
        self.log(f"Created binary test file: {binary_file} ({os.path.getsize(binary_file)} bytes)")
    
    def start_server(self):
        """Start the server process with output capture"""
        self.log("Starting server...")
        
        # Start server process
        self.server_process = subprocess.Popen(
            ["python3", self.server_script, str(self.port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Start output capture threads
        stdout_thread = threading.Thread(
            target=self.server_output.process_output,
            args=(self.server_process.stdout,)
        )
        stderr_thread = threading.Thread(
            target=self.server_output.process_output,
            args=(self.server_process.stderr, "ERROR: ")
        )
        
        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()
        
        # Give server time to start
        time.sleep(2)
        self.log("Server started.", "success")
    
    def stop_server(self):
        """Stop the server process"""
        if self.server_process:
            self.log("Stopping server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.log("Server did not terminate gracefully, forcing...", "error")
                self.server_process.kill()
                self.server_process.wait()
            
            self.server_process = None
            self.log("Server stopped.")
    
    def start_client(self, client_id, input_commands, delay_between_commands=0.5):
        """Start a client process with predefined input commands and output capture"""
        client_name = f"CLIENT{client_id}"
        self.log(f"Starting {client_name}...")
        
        # Create output capture for this client
        color_code = self.COLORS.get(f'client{client_id}', self.COLORS['client1'])
        client_output = OutputCapture(client_name, color_code)
        client_output.start_capture()
        self.client_outputs[client_id] = client_output
        
        # Start client process
        client = subprocess.Popen(
            ["python3", self.client_script, str(self.port)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        self.client_processes.append(client)
        
        # Start output capture threads
        stdout_thread = threading.Thread(
            target=client_output.process_output,
            args=(client.stdout,)
        )
        stderr_thread = threading.Thread(
            target=client_output.process_output,
            args=(client.stderr, "ERROR: ")
        )
        
        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()
        
        # Send commands to client in a separate thread
        def send_commands():
            for cmd in input_commands:
                time.sleep(delay_between_commands)  # Give time for client to process
                client_output.add_output(f"SENDING COMMAND: {cmd}")
                client.stdin.write(cmd + "\n")
                client.stdin.flush()
        
        command_thread = threading.Thread(target=send_commands)
        command_thread.daemon = True
        command_thread.start()
        
        return client
    
    def stop_client(self, client):
        """Stop a specific client process"""
        if client.poll() is None:  # If process is still running
            client.terminate()
            try:
                client.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.log("Client did not terminate gracefully, forcing...", "error")
                client.kill()
                client.wait()
    
    def stop_all_clients(self):
        """Stop all client processes"""
        for client in self.client_processes:
            self.stop_client(client)
        self.client_processes = []
        
        # Stop all client output captures
        for client_id, output in self.client_outputs.items():
            output.stop_capture()
        self.client_outputs = {}
    
    def cleanup(self):
        """Clean up test environment"""
        self.log("Cleaning up test environment...")
        self.stop_all_clients()
        self.stop_server()
        
        # Stop output captures
        self.server_output.stop_capture()
        self.test_output.stop_capture()
        
        # Clean up test files and directories
        if os.path.exists("uploads"):
            shutil.rmtree("uploads")
            os.makedirs("uploads")
        if os.path.exists("downloads"):
            shutil.rmtree("downloads")
            os.makedirs("downloads")
        
        self.log("Cleanup complete.")
    
    def direct_test_file_upload(self, username, password, thread_id, filename, client_id=None):
        """Test file upload directly using sockets with detailed output"""
        client_name = f"CLIENT{client_id}" if client_id else "DIRECT"
        self.log(f"\nTesting direct file upload: {filename} to thread {thread_id} as {username}")
        
        # Create output capture for this operation if needed
        if client_id and client_id not in self.client_outputs:
            color_code = self.COLORS.get(f'client{client_id}', self.COLORS['client1'])
            client_output = OutputCapture(client_name, color_code)
            client_output.start_capture()
            self.client_outputs[client_id] = client_output
        
        # Use existing output capture or test output
        output = self.client_outputs.get(client_id, self.test_output)
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(10)  # Add timeout to prevent hanging
        server_address = (self.server_ip, self.port)
        
        try:
            # Authentication
            auth_msg = f'AUTH {username} {password}'
            output.add_output(f"Sending: {auth_msg}")
            client_socket.sendto(auth_msg.encode(), server_address)
            response, _ = client_socket.recvfrom(4096)
            # Handle binary response safely
            try:
                response_text = response.decode('utf-8', errors='replace')
                output.add_output(f"Auth response: {response_text}")
            except Exception as e:
                output.add_output(f"Auth response: [Binary data, length: {len(response)}]")
            
            # Create thread if it doesn't exist
            create_msg = f'CRT {thread_id}'
            output.add_output(f"Sending: {create_msg}")
            client_socket.sendto(create_msg.encode(), server_address)
            response, _ = client_socket.recvfrom(4096)
            # Handle binary response safely
            try:
                response_text = response.decode('utf-8', errors='replace')
                output.add_output(f"Create thread response: {response_text}")
            except Exception as e:
                output.add_output(f"Create thread response: [Binary data, length: {len(response)}]")
            
            # Send upload request via UDP
            upload_msg = f'UPD {thread_id} {os.path.basename(filename)}'
            output.add_output(f"Sending: {upload_msg}")
            client_socket.sendto(upload_msg.encode(), server_address)
            response, _ = client_socket.recvfrom(4096)
            # Handle binary response safely
            try:
                response_text = response.decode('utf-8', errors='replace')
                output.add_output(f"Upload request response: {response_text}")
                
                # Check if server is ready to receive
                if "Ready to receive" not in response_text:
                    output.add_output(f"Server not ready to receive file: {response_text}")
                    return False
                
                # Extract port from response
                try:
                    port = int(response_text.split("TCP port ")[1].strip())
                except (IndexError, ValueError):
                    port = self.port  # Default to server port if parsing fails
            except Exception as e:
                output.add_output(f"Upload request response: [Binary data, length: {len(response)}]")
                output.add_output(f"Cannot parse response, using default port {self.port}")
                port = self.port
            
            # Create TCP socket for file transfer
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.settimeout(30)  # Longer timeout for file transfer
            tcp_socket.connect((self.server_ip, port))
            
            # Send file metadata
            metadata = {
                'operation': 'upload',
                'username': username,
                'thread_id': thread_id,
                'filename': os.path.basename(filename)
            }
            metadata_json = json.dumps(metadata)
            output.add_output(f"Sending metadata: {metadata_json}")
            tcp_socket.sendall(metadata_json.encode('utf-8') + b'\n\n')
            
            # Send file data in chunks with progress reporting
            file_size = os.path.getsize(filename)
            sent_bytes = 0
            start_time = time.time()
            
            with open(filename, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    tcp_socket.sendall(chunk)
                    
                    sent_bytes += len(chunk)
                    progress = (sent_bytes / file_size) * 100
                    
                    # Report progress at 25%, 50%, 75%, and 100%
                    if int(progress) % 25 == 0 and int(progress) > 0:
                        elapsed = time.time() - start_time
                        speed = sent_bytes / (elapsed * 1024) if elapsed > 0 else 0
                        output.add_output(f"Upload progress: {progress:.1f}% ({sent_bytes}/{file_size} bytes) Speed: {speed:.2f} KB/s")
            
            # Signal end of file
            tcp_socket.shutdown(socket.SHUT_WR)
            
            # Get confirmation with timeout
            tcp_socket.settimeout(10)
            try:
                confirmation_data = tcp_socket.recv(4096)
                # Handle binary response safely
                try:
                    confirmation = confirmation_data.decode('utf-8', errors='replace')
                    output.add_output(f"Upload confirmation: {confirmation}")
                    success = "UPLOAD_SUCCESS" in confirmation
                    if success:
                        output.add_output(f"File {filename} uploaded successfully")
                    else:
                        output.add_output(f"Upload failed: {confirmation}")
                    return success
                except Exception as e:
                    output.add_output(f"Upload confirmation: [Binary data, length: {len(confirmation_data)}]")
                    return False
            except socket.timeout:
                output.add_output("Timeout waiting for upload confirmation")
                return False
            
        except socket.timeout:
            output.add_output("Socket operation timed out")
            return False
        except Exception as e:
            output.add_output(f"Error in file upload test: {str(e)}")
            return False
        finally:
            # Ensure sockets are closed
            try:
                tcp_socket.close()
            except:
                pass
            client_socket.close()
    
    def direct_test_file_download(self, username, password, thread_id, filename, client_id=None):
        """Test file download directly using sockets with detailed output"""
        client_name = f"CLIENT{client_id}" if client_id else "DIRECT"
        self.log(f"\nTesting direct file download: {filename} from thread {thread_id} as {username}")
        
        # Create output capture for this operation if needed
        if client_id and client_id not in self.client_outputs:
            color_code = self.COLORS.get(f'client{client_id}', self.COLORS['client1'])
            client_output = OutputCapture(client_name, color_code)
            client_output.start_capture()
            self.client_outputs[client_id] = client_output
        
        # Use existing output capture or test output
        output = self.client_outputs.get(client_id, self.test_output)
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(10)  # Add timeout to prevent hanging
        server_address = (self.server_ip, self.port)
        
        try:
            # Authentication
            auth_msg = f'AUTH {username} {password}'
            output.add_output(f"Sending: {auth_msg}")
            client_socket.sendto(auth_msg.encode(), server_address)
            response, _ = client_socket.recvfrom(4096)
            # Handle binary response safely
            try:
                response_text = response.decode('utf-8', errors='replace')
                output.add_output(f"Auth response: {response_text}")
            except Exception as e:
                output.add_output(f"Auth response: [Binary data, length: {len(response)}]")
            
            # Send download request via UDP
            download_msg = f'DWN {thread_id} {filename}'
            output.add_output(f"Sending: {download_msg}")
            client_socket.sendto(download_msg.encode(), server_address)
            response, _ = client_socket.recvfrom(4096)
            # Handle binary response safely
            try:
                response_text = response.decode('utf-8', errors='replace')
                output.add_output(f"Download request response: {response_text}")
                
                # Check if server is ready to send
                if "Ready to send" not in response_text:
                    output.add_output(f"Server not ready to send file: {response_text}")
                    return False
                
                # Extract port from response
                try:
                    port = int(response_text.split("TCP port ")[1].strip())
                except (IndexError, ValueError):
                    port = self.port  # Default to server port if parsing fails
            except Exception as e:
                output.add_output(f"Download request response: [Binary data, length: {len(response)}]")
                output.add_output(f"Cannot parse response, using default port {self.port}")
                port = self.port
            
            # Create TCP socket for file transfer
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.settimeout(30)  # Longer timeout for file transfer
            tcp_socket.connect((self.server_ip, port))
            
            # Send file metadata
            metadata = {
                'operation': 'download',
                'username': username,
                'thread_id': thread_id,
                'filename': filename
            }
            metadata_json = json.dumps(metadata)
            output.add_output(f"Sending metadata: {metadata_json}")
            tcp_socket.sendall(metadata_json.encode('utf-8') + b'\n\n')
            
            # Prepare file path
            download_path = os.path.join("downloads", filename)
            
            # Receive file data with progress reporting
            received_bytes = 0
            start_time = time.time()
            
            # First, try to receive the header
            initial_data = b''
            while b'\n' not in initial_data and len(initial_data) < 1024:
                chunk = tcp_socket.recv(1024)
                if not chunk:
                    break
                initial_data += chunk
            
            # Check for FILE_TRANSFER_START header
            if b'FILE_TRANSFER_START' in initial_data or b'FILE_START' in initial_data:
                output.add_output("File transfer started")
                
                # Extract any file data that came with the header
                if b'\n' in initial_data:
                    header, file_data = initial_data.split(b'\n', 1)
                else:
                    file_data = b''
                
                # Receive file data
                with open(download_path, 'wb') as f:
                    # Write any data already received after the header
                    if file_data:
                        f.write(file_data)
                        received_bytes += len(file_data)
                    
                    # Continue receiving data
                    last_progress_report = 0
                    
                    while True:
                        try:
                            chunk = tcp_socket.recv(4096)
                            if not chunk:
                                break
                            
                            f.write(chunk)
                            received_bytes += len(chunk)
                            
                            # Report progress every 100KB
                            if received_bytes - last_progress_report >= 100 * 1024:
                                elapsed = time.time() - start_time
                                speed = received_bytes / (elapsed * 1024) if elapsed > 0 else 0
                                output.add_output(f"Download progress: {received_bytes} bytes received. Speed: {speed:.2f} KB/s")
                                last_progress_report = received_bytes
                                
                        except socket.timeout:
                            output.add_output("Download timed out")
                            return False
                
                # Final progress report
                elapsed = time.time() - start_time
                speed = received_bytes / (elapsed * 1024) if elapsed > 0 else 0
                output.add_output(f"Download complete: {received_bytes} bytes received. Speed: {speed:.2f} KB/s")
                
                if os.path.exists(download_path):
                    output.add_output(f"File downloaded successfully to {download_path}")
                    return True
                else:
                    output.add_output("File download failed - file not found")
                    return False
            else:
                # Handle binary response safely
                try:
                    error_msg = initial_data.decode('utf-8', errors='replace')
                    output.add_output(f"Download failed: {error_msg}")
                except Exception as e:
                    output.add_output(f"Download failed: [Binary data, length: {len(initial_data)}]")
                return False
            
        except socket.timeout:
            output.add_output("Socket operation timed out")
            return False
        except Exception as e:
            output.add_output(f"Error in file download test: {str(e)}")
            return False
        finally:
            # Ensure sockets are closed
            try:
                tcp_socket.close()
            except:
                pass
            client_socket.close()
    
    def run_sequential_test(self):
        """Run sequential client test with detailed output"""
        self.log("\n=== Running Sequential Client Test ===\n", "success")
        
        # Start server
        self.start_server()
        
        try:
            # Client 1 commands (yoda)
            client1_commands = [
                "yoda",                          # username
                "wise@!man",                     # password
                "CRT sequential_test_thread",    # create thread
                "LST",                           # list threads
                "MSG sequential_test_thread This is a test message for sequential testing",  # post message
                "RDT sequential_test_thread",    # read thread
                "EDT sequential_test_thread 1 This is an edited message for sequential testing",  # edit message
                "RDT sequential_test_thread",    # read thread again
                "UPD sequential_test_thread test_files/small.txt",  # upload small file
                "DWN sequential_test_thread small.txt",  # download the file
                "DLT sequential_test_thread 1",  # delete message
                "RDT sequential_test_thread",    # read thread again
                "XIT"                            # exit
            ]
            
            # Start Client 1
            self.log("Starting Client 1 (yoda)...")
            client1 = self.start_client(1, client1_commands)
            
            # Wait for Client 1 to finish
            client1.wait()
            self.log("Client 1 completed.")
            
            # Client 2 commands (r2d2)
            client2_commands = [
                "r2d2",                          # username
                "do*!@#dedo",                    # password
                "LST",                           # list threads
                "CRT sequential_test_thread2",   # create thread
                "MSG sequential_test_thread Response to yoda's message",  # post message
                "RDT sequential_test_thread",    # read thread
                "EDT sequential_test_thread 1 Trying to edit yoda's message",  # edit message (should fail)
                "RDT sequential_test_thread2",   # read thread
                "UPD sequential_test_thread2 test_files/medium.txt",  # upload medium file
                "DWN sequential_test_thread small.txt",  # download yoda's file
                "RMV sequential_test_thread",    # remove thread (should fail)
                "XIT"                            # exit
            ]
            
            # Start Client 2
            self.log("Starting Client 2 (r2d2)...")
            client2 = self.start_client(2, client2_commands)
            
            # Wait for Client 2 to finish
            client2.wait()
            self.log("Client 2 completed.")
            
            # Test large file upload directly
            self.log("Testing large file upload...")
            upload_success = self.direct_test_file_upload("yoda", "wise@!man", "sequential_test_thread", f"{self.test_files_dir}/large.txt", client_id=3)
            
            # Test binary file upload directly
            self.log("Testing binary file upload...")
            upload_success = self.direct_test_file_upload("r2d2", "do*!@#dedo", "sequential_test_thread2", f"{self.test_files_dir}/binary.dat", client_id=4)
            
            # Test file download directly
            self.log("Testing file download...")
            download_success = self.direct_test_file_download("yoda", "wise@!man", "sequential_test_thread2", "medium.txt", client_id=5)
            
            self.log("\nSequential test completed.", "success")
            
        except Exception as e:
            self.log(f"Error in sequential test: {str(e)}", "error")
        finally:
            # Clean up
            self.cleanup()
    
    def run_concurrent_test(self):
        """Run concurrent client test with detailed output"""
        self.log("\n=== Running Concurrent Client Test ===\n", "success")
        
        # Start server
        self.start_server()
        
        try:
            # Client 1 commands (yoda)
            client1_commands = [
                "yoda",                          # username
                "wise@!man",                     # password
                "CRT concurrent_test_thread",    # create thread
                "LST",                           # list threads
                "MSG concurrent_test_thread This is a test message for concurrent testing",  # post message
                "RDT concurrent_test_thread",    # read thread
                "UPD concurrent_test_thread test_files/small.txt",  # upload small file
                "DWN concurrent_test_thread small.txt",  # download the file
                "XIT"                            # exit
            ]
            
            # Client 2 commands (r2d2) - run concurrently
            client2_commands = [
                "r2d2",                          # username
                "do*!@#dedo",                    # password
                "LST",                           # list threads
                "CRT concurrent_test_thread2",   # create thread
                "MSG concurrent_test_thread Response to yoda's message",  # post message
                "RDT concurrent_test_thread",    # read thread
                "UPD concurrent_test_thread2 test_files/medium.txt",  # upload medium file
                "DWN concurrent_test_thread small.txt",  # download yoda's file
                "XIT"                            # exit
            ]
            
            # Client 3 commands (vader) - run concurrently
            client3_commands = [
                "vader",                         # username
                "sithlord**",                    # password
                "LST",                           # list threads
                "CRT concurrent_test_thread3",   # create thread
                "MSG concurrent_test_thread2 Vader's message to r2d2",  # post message
                "RDT concurrent_test_thread",    # read thread
                "RDT concurrent_test_thread2",   # read thread
                "UPD concurrent_test_thread3 test_files/binary.dat",  # upload binary file
                "XIT"                            # exit
            ]
            
            # Start all clients with minimal delay between commands to increase concurrency
            self.log("Starting all clients concurrently...")
            client1 = self.start_client(1, client1_commands, delay_between_commands=0.2)
            client2 = self.start_client(2, client2_commands, delay_between_commands=0.2)
            client3 = self.start_client(3, client3_commands, delay_between_commands=0.2)
            
            # Wait for all clients to finish with timeout
            try:
                self.log("Waiting for clients to complete...")
                client1.wait(timeout=30)
                client2.wait(timeout=30)
                client3.wait(timeout=30)
                self.log("All clients completed successfully.")
            except subprocess.TimeoutExpired:
                self.log("Client timeout expired, terminating clients", "error")
                self.stop_all_clients()
            
            self.log("\nConcurrent test completed.", "success")
            
        except Exception as e:
            self.log(f"Error in concurrent test: {str(e)}", "error")
        finally:
            # Clean up
            self.cleanup()
    
    def run_stress_test(self):
        """Run stress test with many operations and clients"""
        self.log("\n=== Running Stress Test ===\n", "success")
        
        # Start server
        self.start_server()
        
        try:
            # Define users for stress test
            users = [
                {"id": 1, "username": "yoda", "password": "wise@!man"},
                {"id": 2, "username": "r2d2", "password": "do*!@#dedo"},
                {"id": 3, "username": "vader", "password": "sithlord**"},
                {"id": 4, "username": "luke", "password": "light==saber"},
                {"id": 5, "username": "leia", "password": "$blasterpistol$"}
            ]
            
            # Create a thread for each user with many operations
            clients = []
            
            for user in users:
                thread_name = f"stress_thread_{user['id']}"
                
                # Create a mix of commands for stress testing
                commands = [
                    user["username"],                # username
                    user["password"],                # password
                    f"CRT {thread_name}",            # create thread
                    "LST",                           # list threads
                ]
                
                # Add multiple message posts
                for i in range(1, 6):
                    commands.append(f"MSG {thread_name} Message {i} from {user['username']}")
                
                # Read own thread
                commands.append(f"RDT {thread_name}")
                
                # Edit some messages
                commands.append(f"EDT {thread_name} 1 Edited message 1")
                commands.append(f"EDT {thread_name} 3 Edited message 3")
                
                # Read thread again
                commands.append(f"RDT {thread_name}")
                
                # Delete some messages
                commands.append(f"DLT {thread_name} 2")
                commands.append(f"DLT {thread_name} 4")
                
                # Read thread again
                commands.append(f"RDT {thread_name}")
                
                # Upload a file
                file_type = random.choice(["small", "medium", "large"])  # Avoid binary for simplicity
                file_ext = "txt"
                commands.append(f"UPD {thread_name} test_files/{file_type}.{file_ext}")
                
                # Read other threads
                for other_user in users:
                    if other_user["id"] != user["id"]:
                        commands.append(f"RDT stress_thread_{other_user['id']}")
                
                # Download files from other threads
                for other_user in users:
                    if other_user["id"] != user["id"]:
                        other_file_type = random.choice(["small", "medium", "large"])
                        other_file_ext = "txt"
                        commands.append(f"DWN stress_thread_{other_user['id']} {other_file_type}.{other_file_ext}")
                
                # Exit
                commands.append("XIT")
                
                # Start client with minimal delay to increase stress
                self.log(f"Starting stress test client for {user['username']}...")
                client = self.start_client(user["id"], commands, delay_between_commands=0.1)
                clients.append(client)
            
            # Wait for all clients to finish with timeout
            try:
                self.log("Waiting for stress test clients to complete...")
                for i, client in enumerate(clients):
                    self.log(f"Waiting for client {i+1}/{len(clients)}...")
                    client.wait(timeout=60)
                self.log("All stress test clients completed successfully.")
            except subprocess.TimeoutExpired:
                self.log("Client timeout expired, terminating clients", "error")
                self.stop_all_clients()
            
            self.log("\nStress test completed.", "success")
            
        except Exception as e:
            self.log(f"Error in stress test: {str(e)}", "error")
        finally:
            # Clean up
            self.cleanup()
    
    def run_reliability_test(self):
        """Run reliability test with simulated packet loss"""
        self.log("\n=== Running Reliability Test (Simulated Packet Loss) ===\n", "success")
        self.log("Note: This test requires the server and client to implement reliable UDP.")
        self.log("If your implementation doesn't handle packet loss, this test may fail.")
        
        # Start server
        self.start_server()
        
        try:
            # Create a socket patcher to simulate packet loss
            class SocketPatcher:
                def __init__(self, drop_rate=0.2):
                    self.drop_rate = drop_rate
                    self.original_sendto = socket.socket.sendto
                    
                def start_patching(self):
                    def patched_sendto(self, data, *args, **kwargs):
                        if random.random() < self.drop_rate:
                            # Simulate packet loss
                            print(f"\033[91m[PACKET LOSS] Dropped {len(data)} bytes\033[0m")
                            return len(data)
                        return self.original_sendto(data, *args, **kwargs)
                    
                    socket.socket.sendto = patched_sendto
                    
                def stop_patching(self):
                    socket.socket.sendto = self.original_sendto
            
            # Create and start the socket patcher
            patcher = SocketPatcher(drop_rate=0.2)  # 20% packet loss
            patcher.start_patching()
            
            self.log("Socket patched to simulate 20% packet loss")
            
            # Client commands for reliability test
            client_commands = [
                "yoda",                          # username
                "wise@!man",                     # password
                "CRT reliability_test_thread",   # create thread
                "LST",                           # list threads
                "MSG reliability_test_thread This message should survive packet loss",  # post message
                "RDT reliability_test_thread",   # read thread
                "UPD reliability_test_thread test_files/small.txt",  # upload small file
                "DWN reliability_test_thread small.txt",  # download the file
                "XIT"                            # exit
            ]
            
            # Start client
            self.log("Starting client for reliability test...")
            client = self.start_client(1, client_commands, delay_between_commands=1.0)  # Longer delay for reliability test
            
            # Wait for client to finish with extended timeout
            try:
                self.log("Waiting for reliability test client to complete...")
                client.wait(timeout=60)
                self.log("Reliability test client completed successfully.")
            except subprocess.TimeoutExpired:
                self.log("Client timeout expired, terminating client", "error")
                self.stop_all_clients()
            
            # Stop the socket patcher
            patcher.stop_patching()
            self.log("Socket restored to normal operation")
            
            self.log("\nReliability test completed.", "success")
            
        except Exception as e:
            self.log(f"Error in reliability test: {str(e)}", "error")
        finally:
            # Clean up
            self.cleanup()
    
    def run_error_handling_test(self):
        """Run test for error handling with invalid commands and edge cases"""
        self.log("\n=== Running Error Handling Test ===\n", "success")
        
        # Start server
        self.start_server()
        
        try:
            # Client commands with invalid operations
            client_commands = [
                "yoda",                          # username
                "wise@!man",                     # password
                "INVALID_COMMAND",               # invalid command
                "CRT",                           # missing thread name
                "CRT error_test_thread",         # valid create thread
                "MSG",                           # missing thread and message
                "MSG error_test_thread",         # missing message
                "MSG nonexistent_thread Test message",  # nonexistent thread
                "RDT",                           # missing thread name
                "RDT nonexistent_thread",        # nonexistent thread
                "EDT",                           # missing all parameters
                "EDT error_test_thread",         # missing message id and content
                "EDT error_test_thread 1",       # missing content
                "EDT error_test_thread 999 Test edit",  # nonexistent message id
                "DLT",                           # missing all parameters
                "DLT error_test_thread",         # missing message id
                "DLT error_test_thread 999",     # nonexistent message id
                "UPD",                           # missing all parameters
                "UPD error_test_thread",         # missing filename
                "UPD error_test_thread nonexistent_file.txt",  # nonexistent file
                "DWN",                           # missing all parameters
                "DWN error_test_thread",         # missing filename
                "DWN error_test_thread nonexistent_file.txt",  # nonexistent file
                "RMV",                           # missing thread name
                "RMV nonexistent_thread",        # nonexistent thread
                "XIT"                            # exit
            ]
            
            # Start client
            self.log("Starting client for error handling test...")
            client = self.start_client(1, client_commands)
            
            # Wait for client to finish
            client.wait()
            self.log("Error handling test client completed.")
            
            self.log("\nError handling test completed.", "success")
            
        except Exception as e:
            self.log(f"Error in error handling test: {str(e)}", "error")
        finally:
            # Clean up
            self.cleanup()
    
    def run_all_tests(self):
        """Run all tests sequentially"""
        self.log("\n=== Running All Tests ===\n", "success")
        
        # Run sequential test
        self.run_sequential_test()
        
        # Run concurrent test
        self.run_concurrent_test()
        
        # Run stress test
        self.run_stress_test()
        
        # Run reliability test
        self.run_reliability_test()
        
        # Run error handling test
        self.run_error_handling_test()
        
        self.log("\nAll tests completed.", "success")

def main():
    """Main function to parse arguments and run tests"""
    parser = argparse.ArgumentParser(description='Enhanced Autotest for Discussion Forum Application')
    parser.add_argument('--server', default='server.py', help='Server script filename')
    parser.add_argument('--client', default='client.py', help='Client script filename')
    parser.add_argument('--port', type=int, default=6000, help='Port number to use')
    parser.add_argument('--test', choices=['sequential', 'concurrent', 'stress', 'reliability', 'error', 'all'], 
                        default='all', help='Test to run')
    
    args = parser.parse_args()
    
    # Create and run the autotest
    autotest = EnhancedAutoTest(args.server, args.client, args.port)
    
    # Run the selected test
    if args.test == 'sequential':
        autotest.run_sequential_test()
    elif args.test == 'concurrent':
        autotest.run_concurrent_test()
    elif args.test == 'stress':
        autotest.run_stress_test()
    elif args.test == 'reliability':
        autotest.run_reliability_test()
    elif args.test == 'error':
        autotest.run_error_handling_test()
    else:  # 'all'
        autotest.run_all_tests()

if __name__ == "__main__":
    main()
