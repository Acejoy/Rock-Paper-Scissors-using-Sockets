import socket

PORT = 10000
IP = '127.0.0.1'

player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
player.connect((IP, PORT))

'''
symbol to val mapping
Rock : 1
Scissors : 2
Paper : 3
'''
dict_entry = {'ROCK':1, 'PAPER':3, 'SCISSORS':2}

data = player.recv(1024).decode()
print('SERVER>>>'+data)

while True:
    choice=input('YOU>>>').upper()
    if choice in ['ROCK', 'PAPER', 'SCISSORS']:
        player.sendall(str(dict_entry.get(choice)).encode())
        break
    else:
        print('Wrong Input.')

res = player.recv(1024).decode()
print('SERVER>>>'+res)
player.close()