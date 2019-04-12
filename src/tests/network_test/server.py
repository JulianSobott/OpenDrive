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
conn = socket.socket()
conn.bind(adress)
conn.listen(1)
print("Server hoert jetzt")
try:
    client, client_adress = conn.accept()
    print(f"neuer Client verbunden: {client_adress}")
    try:
        while True:
            data = client.recv(1024)
            if data == b"bye":
                break
            # example = b"hallo das ist ein test"

            print(str(data, "utf-8"))
            #answer = input(">>>")
            answer = f"ich habe das für dich bei meiner web suche gefunden {str(data,'utf-8')}"
            client.send(bytes(answer, "utf-8"))
    finally:
        client.close()
finally:
    conn.close()
