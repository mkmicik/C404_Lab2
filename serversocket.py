#!/usr/bin/env python

import socket, os, select

serverSocket = socket.socket(
	socket.AF_INET, 			# socket on the internet (IP protocol)
	socket.SOCK_STREAM)			# specifies TCP (stream abstraction)

serverSocket.bind((
	"0.0.0.0", 			# broadcast to all addresses  
	12345				# port number
	))

serverSocket.listen(5)

while True:
	print "Waiting for connection..."
	(incomingSocket, address) = serverSocket.accept()		# blocking wait for connection
	print "We got a connection from %s" % (str (address))

	pid = os.fork()

	if pid == 0:
		# child process
		outgoingSocket = socket.socket(
			socket.AF_INET, 			# socket on the internet (IP protocol)
			socket.SOCK_STREAM)			# specifies TCP (stream abstraction)

		outgoingSocket.connect(("www.google.com", 80)) # connect to google on port 80

		request = bytearray()
		while True:
			incomingSocket.setblocking(0)
			try:
				part = incomingSocket.recv(1024)		# specifies we receive 1024 bytes at a time
			except IOError, exception:
				if exception.errno == 11:
					part = None
				else:
					raise

			if (part):					# if we got anything, append it to our buffer 
				request.extend(part)
				outgoingSocket.sendall(part)
			#else:
			#	break		# when we stop receiving bytes, break out of the loop
			
			outgoingSocket.setblocking(0)

			try:
				part = outgoingSocket.recv(1024)		# specifies we receive 1024 bytes at a time
			except IOError, exception:
				if exception.errno == 11:
					part = None
				else:
					raise

			
			if (part):					# if we got anything, append it to our buffer 
				incomingSocket.sendall(part)
			select.select(
				[incomingSocket, outgoingSocket],
				[],
				[incomingSocket, outgoingSocket],
				1)
			#else:
			#	break		# when we stop receiving bytes, break out of the loop

		print request
		#sys.exit(0)
	#else:
		# parent process