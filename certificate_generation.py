

"""Chat server for CST311 Programming Assignment 4"""
__author__ = "Team 2"
__credits__ = [
  "Henry Garkanian",
  "Ivan Soria",
  "Kyle Stefun",
  "Bryan Zanoli"
]

import subprocess
from getpass import getpass
PASSPHRASE = "CST311"


# define main function
def main():
    #prompt useer for a common name
    #for a chat server
    common_name = input("Enter a common name: ")

    #check to see if common_name.txt exists
    #if it does, overwrite the contents with the new common name
    with open("./common_name.txt", "w") as f:
        f.write(common_name)

    #add the common name and ip address to the /etc/hosts file\
    add_to_hosts()

    #generate a private key for the server
    # using the provided passphrase
    #PASSPHRASE = 
    generate_private_key()

    #generate a certificate signing request (CSR)
    #for the server using the provided passphrase
    generate_csr(PASSPHRASE)

    #generate a certificate for the server using the
    generate_certificate()


# Write a function or set of commands to add the IP addresses and common name of the server to the /etc/hosts file.
# This step requires administrative privileges, so make sure to use sudo.
def add_to_hosts():
    # Read the common name from the file
    with open("./common_name.txt", "r") as f:
        common_name = f.readline().strip()
    
   # Define the IP address of the server
    server_ip = "10.0.2.14"  
    
    # Construct the entry
    hosts_entry = f"{server_ip} {common_name}"
    
    # Command to append the entry to /etc/hosts
    command = f"echo '{hosts_entry}' | sudo tee -a /etc/hosts"
    
    # Run the command
    subprocess.run(command, shell=True, check=True)

# Define a function to generate a private key for the
# server using the openssl genrsa command.def 
def generate_private_key():
    #prompt user for a passphrase, mask the input
    #PASSPHRASE = getpass("Enter a passphrase for tpa4.chat.test-key.pem: ")

    # Command to generate the private key
    command = f"openssl genrsa -aes256 -out tpa4.chat.test-key.pem -passout pass:{PASSPHRASE} 2048"

    # Run the command
    subprocess.run(command, shell=True, check=True)

    return PASSPHRASE

#Create a function to generate certificate signing 
#requests (CSRs) for the server.
# You’ll need to use the openssl req command with the 
#appropriate options and subject details.
def generate_csr(PASSPHRASE):

    #get the common name from the file
    with open("./common_name.txt", "r") as f:
        common_name = f.readline().strip()

    # Command to generate the CSR
    #command = f"openssl req -nodes -new -config /etc/ssl/openssl.cnf -key tpa4.chat.test-key.pem -out tpa4.chat.test.csr -passin pass:{PASSPHRASE} -subj '/C=US/ST=CA/L=Seaside/O=CST311/OU=Networking/CN={common_name}'"
    
    # Command to generate the CSR
    command = [
        "openssl", "req", "-nodes", "-new", "-config" ,"/etc/ssl/openssl.cnf",
        "-key", "tpa4.chat.test-key.pem",
        "-out", "tpa4.chat.test.csr",
        "-passin", f"pass:{PASSPHRASE}",
        "-subj", f"/C=US/ST=CA/L=Seaside/O=CST311/OU=Networking/CN={common_name}"
    ]

    # Run the command
    subprocess.run(command, check=True)

#Write a function to generate a certificate from the 
#CSRs using the openssl x509 command. This will also 
#involve specifying the CA certificate and private key.
def generate_certificate():
    # Command to generate the certificate
    #command = f"openssl x509 -req -days 365 -in tpa4.chat.test.csr -CA /etc/ssl/demoCA/cacert.pem -CAkey /etc/ssl/demoCA/private/cakey.pem -CAcreateserial -out tpa4.chat.test-key.pem -passin pass:{PASSPHRASE}"

    # Command to generate the certificate
    command = [
        "openssl", "x509", "-req",
        "-in", "tpa4.chat.test.csr",
        "-CA", "/etc/ssl/demoCA/cacert.pem",
        "-CAkey", "/etc/ssl/demoCA//private/cakey.pem",
        "-CAcreateserial",
        "-out", "tpa4.chat.test.pem", #UPDATED
        "-days", "365"
    ]

    # Run the command
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()