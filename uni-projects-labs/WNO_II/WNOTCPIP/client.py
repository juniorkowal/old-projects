import socket
import threading
import os

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1', 23160)
        print(f"Polaczono z {server_address[0]} na porcie {server_address[1]}")
        self.socket.connect(server_address)

    def sending_msg(self):
        while True:
            message_sent=input()
            message=message_sent.encode(encoding='utf-8')
            if '.doc' in message_sent:
                file_data=open((os.getcwd()+"/to_send/"+str(message_sent)),'rb')
                message=message+file_data.read()
                print(f"Wysylanie pliku: '{message_sent}'")
                file_data.close()
            else:
                print(f"Wysylanie: '{message.decode(encoding='utf-8')}'")
            self.socket.sendall(message)

    def receive_msg(self):
        while True:
            data_received=0
            data_expected=1024
            while data_received<data_expected:
                data=self.socket.recv(1024)
                data_received+=len(data)
                print(f"Otrzymano: '{data.decode(encoding='utf-8')}'")

    def launch(self):
        threads = []
        thread1 = threading.Thread(target=self.sending_msg)
        threads.append(thread1)
        thread1.start()
        thread2 = threading.Thread(target=self.receive_msg)
        threads.append(thread2)
        thread2.start()

if __name__ == '__main__':
    client = Client()
    client.launch()