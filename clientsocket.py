#!/usr/bin/env python

import socket

clientSocket = socket.socket(
	socket.AF_INET, 			# socket on the internet (IP protocol)
	socket.SOCK_STREAM)			# specifies TCP (stream abstraction)

clientSocket.connect(("www.google.com", 80)) # connect to google on port 80

request = "GET / HTTP/1.0\n\n"

clientSocket.sendall(request)

response = bytearray()

while True:
	part = clientSocket.recv(1024)		# specifies we receive 1024 bytes at a time
	if (part):					# if we got anything, append it to our buffer 
		response.extend(part)
	else:
		break		# when we stop receiving bytes, break out of the loop

print response