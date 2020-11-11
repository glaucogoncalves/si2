import socket

site = "www.google.com.br"

mysock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
mysock.connect((site,80))

msg = "GETE / HTTP/1.0\n"
msg = msg + "Host: "+site+"\n"
msg = msg + "\n"

mysock.send(msg.encode("ascii"))

data = mysock.recv(1000)
print(data.decode())
    
mysock.close()
