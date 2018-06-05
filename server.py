import socket
import time

s = socket.socket()

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)
print("socket is listening")

# a forever loop until we interrupt it or
# an error occurs
while True:

   # Establish connection with client.
   c, addr = s.accept()
   print('Got connection from', addr)

   # send a thank you message to the client.
   c.send(b"HTTP/1.1 200 OK\n"
         +b"Content-Type: text/html\n"
         +b"\n" # Important!
         +b"<html><body>Hello World</body></html>\n")
   time.sleep(1)
   c.send
   c.close()
