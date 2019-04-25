# TCP Client
import socket
import library
import sys

CLIENT_PORT = 9000
SERVER_PORT = 7777
BUFFER = 1024

HOSTS = {
  1: 'fdce:1d24:321:0:e5fa:2e62:9a5a:9984',
  2: 'fdce:1d24:321:0:d480:12f9:3c23:3e3f',
  3: '::'
}

# HOSTS = {
#   1: '::',
#   2: '::',
#   3: '::'
# }

def usage():
  print("Usage: python client.py <device number>")
  exit(-1)

def main():
  if len(sys.argv) != 2:
    usage()
  
  key = int(sys.argv[1])

  while (True):
    # Create a client socket to interact with server
    client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    client_socket.connect((HOSTS[key], SERVER_PORT))
    filepath = input('Filepath: ')
    filename = input('Save as: ')
    # Send filepath to server through client socket
    client_socket.send(filepath.encode())

    # Write data being received to file
    with open(filename.strip(), 'wb') as f:
      # Capture data while server is still sending it
      data = client_socket.recv(BUFFER)
      if (data == 'Error processing command'):
        print('Error retrieving data')
        break
      while (data):
        print('Receiving data...')
        f.write(data)
        data = client_socket.recv(BUFFER)
        if not data:
          break

    # Cleanup and close
    print('File successfully saved as %s' % filename)
    client_socket.close()

    # Prompt for reentry
    while True:
      decision = input('Continue? [y/n]')
      if decision == 'y':
        break
      if decision == 'n':
        return
      else: continue

# Run code
main()