"""
:module: 
:synopsis: "Kurzbeschreibung"
:author: Julien Wagler
    
public functions
-----------------

.. autofunction:: "Name der Funktion"


private functions
------------------

.. autofunction:: "Name der Funktion"



"""
import socket
adress = "localhost", 5002
server = socket.socket()
server.connect(adress)
print("erfolgreich verbunden")
try:
    while True:
        request = input(">>>")
        server.send(bytes(request, "utf-8"))
        if request == "bye":
            print("client beendet")
            break
        data = server.recv(1024)
        print(str(data, "utf-8"))

finally:
    server.close()
