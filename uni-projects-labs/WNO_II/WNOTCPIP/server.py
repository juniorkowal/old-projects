import socket
import threading
import os

class Server:
    def __init__(self):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_address=('127.0.0.1',23160)
        print(f"Serwer dziala na adresie: {server_address[0]}, na porcie {server_address[1]}")
        self.socket.bind(server_address)
        self.socket.listen()
        print("Czekanie na polaczenie ...")
        self.connections=[]

    def sending_msg(self):
        while True:
            message_sent=input()
            message=message_sent.encode(encoding='utf-8')
            print(f"Wysylanie wiadomosci: '{(message.decode(encoding='utf-8'))}'")
            for i in range (len(self.connections)):
                self.connections[i][0].sendall(message)

    def receive_msg(self,connection,address):
        while True:
            data=connection.recv(1024)
            test_if_doc=data.decode(encoding='utf-8',errors='ignore')
            if '.doc' in test_if_doc:
                filename=test_if_doc.split('.')[0]+'.doc'
                print(f"Odebrano plik '{filename}' z portu {address[1]}")
                while True:
                    temp=connection.recv(1024)
                    data+=temp
                    if len(temp)<1024:
                        break
                file=open((os.getcwd()+"/received/"+str(filename)),'wb')
                file.write(data[len(filename):])
                file.close()
                data=f"Plik: '{filename}' zostal przeslany na serwer z portu {address[1]}".encode(encoding='utf-8')
            else:
                print(f"Odebrano wiadomosc: '{data.decode(encoding='utf-8')}' z portu {address[1]}")
            for i in range(len(self.connections)):
                if self.connections[i][1]==address:
                    continue
                self.connections[i][0].send(data)

    def launch(self):
        while True:
            conn,address=self.socket.accept()
            thread1=threading.Thread(target=self.sending_msg)
            thread1.start()
            thread2=threading.Thread(target=self.receive_msg,args=(conn,address))
            thread2.start()
            self.connections.append((conn,address))
            print("Polaczono z: ", address)
if __name__ == '__main__':
    server=Server()
    server.launch()
