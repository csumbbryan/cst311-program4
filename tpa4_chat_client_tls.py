#!env python

"""Chat client for CST311 Programming Assignment 4"""
__author__ = "Team 2"
__credits__ = [
  "Henry Garkanian",
  "Ivan Soria",
  "Kyle Stefun",
  "Bryan Zanoli"
]

import socket as s
import _thread
import time
import ssl

# Configure logging.
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Set global variables.
server_name = "tpa4.chat.test" #UPDATED
server_port = 12000
complete = 0
serverKey = "tpa4.chat.test-key.pem"
serverCert = "tpa4.chat.test.pem"
client_cert_file = "/etc/ssl/demoCA/cacert.pem"

# SETUP CONTEXT
context = ssl.create_default_context()
#context.verify_mode = ssl.CERT_REQUIRED
#context.load_cert_chain(certfile=serverCert,keyfile=serverKey)
context.load_verify_locations(cafile=client_cert_file)
#context.keylog_filename="/home/mininet/CST311/program4/tlskeylogfile" #FILEPATH NEEDS TO BE UPDATED

def client_input(client_socket):
  try:
    print("Welcome to the chat! To send a message, type the message and click enter.") 

    # Get input from user.
    while True: 
      user_input = input()
      # Set data across socket to server.
      # Note: encode() converts the string to UTF-8 for transmission.
      client_socket.send(user_input.encode())
      if (user_input == 'bye'):
        complete = 1
        break
  finally:
    print()

def client_receive(client_socket):
  try:
    while True:  
      # Read response from server.
      server_response = client_socket.recv(1024)
      # Decode server response from UTF-8 bytestream.
      server_response_decoded = server_response.decode()
      # Print output from server.
      print(server_response_decoded)
      # Check for disconnected socket.
  except OSError as e:
    log.info("Client socket no longer open")
  finally:
    print()

def main():
  # Create socket.
  client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
  client_socket = context.wrap_socket(client_socket, server_hostname=server_name)
  
  try:
    # Establish TCP connection.
    client_socket.connect((server_name,server_port))
    #ADDED FOR TLS:
    
  # Log error if client socket cannot be established
  except Exception as e:
    log.exception(e)
    log.error("***Advice:***")
    if isinstance(e, s.gaierror):
      log.error("\tCheck that server_name and server_port are set correctly.")
    elif isinstance(e, ConnectionRefusedError):
      log.error("\tCheck that server is running and the address is correct")
    else:
      log.error("\tNo specific advice, please contact teaching staff and include text of error and code.")
    exit(8)
  
  # Start separate threads for client input (send) and client receive to 
  # ensure bidirectional communication
  _thread.start_new_thread(client_input, (client_socket,)) 
  _thread.start_new_thread(client_receive, (client_socket,))
  
  # Wait for client to finish, then close the socket
  while True:
    if (complete == 1):
      break
    time.sleep(.5)
  client_socket.close()

# This helps shield code from running when we import the module.
if __name__ == "__main__":
  main()
    