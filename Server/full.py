import socket as k
import os

s = k.socket()
s.bind(("", 8080))
s.listen(5)

while 1:
  c=s.accept()[0]
  path='.'+c.recv(1024).decode().split()[1]
  if ".." or "//" in path: c.send(b"HTTP/1.1 403 Forbidden")
  elif path.endswith("/"): 
    t=f"<html><body><h1>Directory listing of {path[1:]}:</h1><br>"
    for f in os.listdir(path):
      if f!="index.html": t+=f"<a href='{f}'>{f}</a><br>"
      else: path+="index.html"
    t+="</body></html>"
    c.send(b"HTTP/1.1 200 OK\n\n"+t.encode())
  else:
    try:
      with open(path, 'rb') as f:
        o=f.read()
        c.send(b"HTTP/1.1 200 OK\n\n"+o)
        f.close()
    except: c.send(b"HTTP/1.1 404 Not Found")
  c.close()
