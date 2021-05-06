import tkinter as tk
import socket
import threading
from PIL import ImageTk, Image

PORT = 10000
IP = '127.0.0.1'
Font_tuple1 = ("Comic Sans MS", 20, "bold")
Font_tuple2 = ("Comic Sans MS", 13)


'''
symbol to val mapping
Rock : 1
Scissors : 2
Paper : 3
'''
dict_entry = {'ROCK':1, 'PAPER':3, 'SCISSORS':2}


class Gui:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Rock Paper Scissors Game')
        self.window.config(bg='#7092be')
        self.window.geometry('530x550')
        self.window.resizable(False, False)
        
        self.label_Head = tk.Label(self.window,text='Rock, Paper, Scissors !!!', bg='#7092be', font=Font_tuple1)
        self.rock_img = self.get_img('./pics/rock.png')
        self.paper_img = self.get_img('./pics/paper.png')
        self.scissor_img = self.get_img('./pics/scissors.png')               

        ##creating buttons
        self.rock_btn = tk.Button(self.window,bd=0, highlightthickness=0,image=self.rock_img,
                                    state=tk.DISABLED, command=lambda: self.set_value(1))
        self.paper_btn = tk.Button(self.window,bd=0, highlightthickness=0,image=self.paper_img,
                                    state=tk.DISABLED, command=lambda: self.set_value(3))
        self.scissor_btn = tk.Button(self.window,bd=0, highlightthickness=0,image=self.scissor_img,
                                    state=tk.DISABLED, command=lambda: self.set_value(2))
        
        self.btn_list = [self.rock_btn, self.scissor_btn, self.paper_btn]

        self.symbol_chosen = None
        self.label_chosen = tk.Label(self.window,fg='white', font=Font_tuple2, bg='#7092be')


        self.label_result = tk.Label(self.window,fg='red', font=Font_tuple1, bg='#7092be')


        ##placing the widgets
        self.label_Head.place(x=100, y=100)
        self.rock_btn.place(x=50, y=200)
        self.scissor_btn.place(x=200, y=200)
        self.paper_btn.place(x=350, y=200)
        self.label_chosen.place(x=195, y=320)
        self.label_result.place(x=195, y=400)
        
        self.player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player.connect((IP, PORT))
        self.start_game()
        self.window.mainloop()

    def start_game(self):      

        client_thread = threading.Thread(target=self.handle_connection)
        client_thread.start()
        

    def get_img(self,img_path):
        img = Image.open(img_path)
        resized_img = img.resize((100,100), Image.ANTIALIAS)
        res_img = ImageTk.PhotoImage(resized_img)

        return res_img

    def set_value(self, num):
        self.symbol_chosen = num

        for btn in self.btn_list:
            btn.config(state=tk.DISABLED)

        if num==1:
            self.label_chosen.config(text='You chose Rock')
        elif num==2:
            self.label_chosen.config(text='You chose Scissors')
        if num==3:
            self.label_chosen.config(text='You chose Paper')    
        
    def enable_btns(self):
        for btn in self.btn_list:
            btn.config(state=tk.NORMAL)


    def set_result(self, result):
        self.label_result.config(text=result)

        pass

    def handle_connection(self):
        data = self.player.recv(1024).decode()
        self.enable_btns()

        while self.symbol_chosen == None:
            pass
        
        self.player.sendall(str(self.symbol_chosen).encode())
        res = self.player.recv(1024).decode()
        self.set_result(res)
        self.player.close()


    

if __name__ == "__main__":
    gui = Gui()
