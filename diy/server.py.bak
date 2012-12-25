import socket

host = 'localhost'
port = 1025

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(1)

print('Server is run on %d; press Ctrl + C end' %port)

while 1:
	clientsock, clientaddr = s.accept()
	clientfile = clientsock.makefile('rw', 0)
	clientfile.write('welcom, ' + str(clientaddr) + '\n')
	clientfile.write('please enter a string:')
	line = clientfile.readline().strip()
	clientfile.write('you enter %d characters\n' %len(line))
	clientfile.close()
	clientsock.close()
