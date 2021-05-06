import socket
import threading

PORT = 10000
IP = '127.0.0.1'

game_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
game_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
game_server.bind((IP, PORT))

clients_list = []
threads_list = []
'''
symbol to val mapping
Rock : 1
Scissors : 2
Paper : 3
'''

class Client:

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.entry = 0
 

def handle_client(conn, addr):
    global clients_list
    client = Client(conn, addr)
    clients_list.append(client)
    print(f'[QUERYING] Sending message to client.......{addr}')
    try:
        client.conn.sendall('Enter your Entry[Rock, Paper, Scissors]'.encode())
        entry = client.conn.recv(1024).decode()
        entry = int(entry)
        client.entry = entry
        print(f'[ENTRY RECIEVED] from {client.addr}')
    except:
        #print(f'[CONNECTION LOST] by {addr}')
        clients_list.remove(client)
        #print('Len:',len(clients_list))
        client.conn.close()
        

    
def listen_connection():
    game_server.listen()
    print('[LISTENING] the Server is waiting for connection.........')

    while len(clients_list)<2:
        conn, addr = game_server.accept()
        print(f'[CONNECTED] to {addr}')
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        threads_list.append(thread)
        thread.start()
        print(f'[ACTIVE CONNECTIONS] :{threading.activeCount()-1}')

    print('[ALL PLAYERS JOINED].........')

def judge_entries():

    entries_left = True
    
    while entries_left:
        if 0 not in [clients_list[0].entry, clients_list[1].entry]:
            entries_left = False

    conn_to_res = ['', '']

    entries = (clients_list[0].entry, clients_list[1].entry)

    if entries[0]==entries[1]:
        conn_to_res[0] = 'Draw'
        conn_to_res[1] = 'Draw'
    if entries==(1,2):
        conn_to_res[0] = 'You Won'
        conn_to_res[1] = 'You Lost'
    elif entries==(2,1):
        conn_to_res[1] = 'You Won'
        conn_to_res[0] = 'You Lost'
    elif entries==(1,3):
        conn_to_res[1] = 'You Won'
        conn_to_res[0] = 'You Lost'
    elif entries==(3,1):
        conn_to_res[0] = 'You Won'
        conn_to_res[1] = 'You Lost'
    elif entries==(2,3):
        conn_to_res[0] = 'You Won'
        conn_to_res[1] = 'You Lost'
    elif entries==(3,2):
        conn_to_res[1] = 'You Won'
        conn_to_res[0] = 'You Lost'

    print(f'[CONNECTION CLOSED] to {clients_list[0].addr}')
    clients_list[0].conn.sendall(conn_to_res[0].encode())
    print(f'[CONNECTION CLOSED] to {clients_list[1].addr}')
    clients_list[1].conn.sendall(conn_to_res[1].encode())
    
    clients_list[0].conn.close()
    clients_list[1].conn.close()


def evaluate():
    #print('Len:',len(clients_list))
    #print(clients_list)
    
    ##waiting for all the threads to complete execution
    for th in threads_list:
        th.join()

    if len(clients_list)<2:
        print('[ERROR OCCURRED] Client/s abruptly ended connection')

        if len(clients_list) == 1:
            clients_list[0].conn.sendall('Other Player ended connection.'.encode())
            clients_list[0].conn.close()
    else:
        judge_entries()

        
listen_connection()
evaluate()

print('[SERVER CLOSING] ....')
game_server.close()


