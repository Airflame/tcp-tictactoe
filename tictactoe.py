import socket
import time
import _thread as thread
from tkinter import *
from tkinter import ttk

def ipv4(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False
    return True

def nan(arg):
    try:
        arg = int(arg)
    except ValueError:
        return True
    else:
        return False

def win(board):
    wlist = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for i in range(len(wlist)):
        row = [board[j] for j in wlist[i]]
        if 0 not in row and row[0] == row[1] == row[2]:
            return row[0]
    return 0


class ClientApp(object):
    def __init__(self, master):
        self.root = master
        self.root.resizable(False, False)
        self.root.title("Client")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.content = ttk.Frame(self.root)
        self.label = Label(self.content, text="Enter server's IP")
        self.fields = [Button(self.content, text="", width=8, height=4) for i in range(9)]
        self.entry_text = StringVar(self.root, value="127.0.0.1")
        self.entry = Entry(self.root, textvariable=self.entry_text)
        self.entry_button = Button(self.root, text="Connect", command=lambda: self.b_cn())
        self.content.grid(column=0, row=0)
        self.label.grid(row=3, columnspan=3)
        self.entry.grid(row=4, column=0)
        self.entry_button.grid(row=4, column=1)
        self.fields[0].config(command=lambda: self.b_mv(0))
        self.fields[1].config(command=lambda: self.b_mv(1))
        self.fields[2].config(command=lambda: self.b_mv(2))
        self.fields[3].config(command=lambda: self.b_mv(3))
        self.fields[4].config(command=lambda: self.b_mv(4))
        self.fields[5].config(command=lambda: self.b_mv(5))
        self.fields[6].config(command=lambda: self.b_mv(6))
        self.fields[7].config(command=lambda: self.b_mv(7))
        self.fields[8].config(command=lambda: self.b_mv(8))
        for i in range(9):
            self.fields[i].grid(column=int(i / 3), row=int(i % 3))
        thread.start_new_thread(self.loop, ())

    def on_closing(self):
        self.root.destroy()
        exit()

    def b_mv(self, bid):
        self.move = bid

    def b_cn(self):
        self.addr = self.entry_text.get()

    def loop(self):
        for obj in self.fields:
            obj.configure(state=DISABLED)
        self.connection = False
        self.addr = "x"
        while not self.connection:
            while not ipv4(self.addr):
                pass
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.label.config(text="Waiting for connection")
            try:
                self.serverSocket.connect((self.addr, 7777))
            except:
                self.label.config(text="Connection error")
            else:
                self.label.config(text="Connected")
                self.connection = True
        self.entry.configure(state=DISABLED)
        self.entry_button.configure(state=DISABLED)
        while True:
            self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            while 0 in self.board:
                self.label.config(text="Enemy's turn")
                for obj in self.fields:
                    obj.configure(state=DISABLED)
                try:
                    self.buf = self.serverSocket.recv(26)
                except socket.error:
                    for obj in self.fields:
                        obj.configure(state=DISABLED)
                    self.label.config(text="Connection lost")
                    while True:
                        pass
                self.exmove = int(self.buf.decode('ascii'))
                del self.buf
                self.board[self.exmove] = -1
                self.fields[self.exmove].config(text="X")
                if win(self.board) != 0 or 0 not in self.board:
                    break

                self.label.config(text="Your turn")
                for obj in self.fields:
                    obj.configure(state=NORMAL)
                self.move = -1
                while self.move not in range(9) or self.board[self.move] != 0:
                    pass
                self.board[self.move] = 1
                self.fields[self.move].config(text="O")
                self.msg = str(self.move)
                try:
                    self.serverSocket.send(self.msg.encode('ascii'))
                except socket.error:
                    for obj in self.fields:
                        obj.configure(state=DISABLED)
                    self.label.config(text="Connection lost")
                    while True:
                        pass
                if win(self.board) != 0 or 0 not in self.board:
                    break

            for obj in self.fields:
                obj.configure(state=DISABLED)
            if win(self.board) == 1:
                self.label.config(text="You won")
            elif win(self.board) == 0:
                self.label.config(text="Draw")
            elif win(self.board) == -1:
                self.label.config(text="You lost")
            time.sleep(1)
            self.label.config(text="Restarting")
            time.sleep(1)
            for obj in self.fields:
                obj.config(text="")


class ServerApp(object):
    def __init__(self, master):
        self.root = master
        self.root.resizable(False, False)
        self.root.title("Server")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.content = ttk.Frame(self.root)
        self.label = Label(self.content, text="...")
        self.fields = [Button(self.content, text="", width=8, height=4) for i in range(9)]
        self.content.grid(column=0, row=0)
        self.label.grid(row=3, columnspan=3)
        self.fields[0].config(command=lambda: self.b_mv(0))
        self.fields[1].config(command=lambda: self.b_mv(1))
        self.fields[2].config(command=lambda: self.b_mv(2))
        self.fields[3].config(command=lambda: self.b_mv(3))
        self.fields[4].config(command=lambda: self.b_mv(4))
        self.fields[5].config(command=lambda: self.b_mv(5))
        self.fields[6].config(command=lambda: self.b_mv(6))
        self.fields[7].config(command=lambda: self.b_mv(7))
        self.fields[8].config(command=lambda: self.b_mv(8))
        for i in range(9):
            self.fields[i].grid(column=int(i / 3), row=int(i % 3))
        thread.start_new_thread(self.loop, ())

    def on_closing(self):
        self.root.destroy()
        exit()

    def b_mv(self, bid):
        self.move = bid

    def loop(self):
        for obj in self.fields:
            obj.configure(state=DISABLED)
        self.serverSocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('', 7777))
        self.serverSocket.listen()
        self.label.config(text="Waiting for connection")
        self.clientSocket, self.addr = self.serverSocket.accept()
        self.label.config(text="Connected with {}".format(str(self.addr)) + "\n")
        while True:
            self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            while 0 in self.board:
                self.label.config(text="Your turn")
                for obj in self.fields:
                    obj.configure(state=NORMAL)
                self.move = -1
                while self.move not in range(9) or self.board[self.move] != 0:
                    pass
                self.board[self.move] = 1
                self.fields[self.move].config(text="X")
                self.msg = str(self.move)
                try:
                    self.clientSocket.send(self.msg.encode('ascii'))
                except socket.error:
                    for obj in self.fields:
                        obj.configure(state=DISABLED)
                    self.label.config(text="Connection lost")
                    while True:
                        pass
                if win(self.board) != 0 or 0 not in self.board:
                    break

                self.label.config(text="Enemy's turn")
                for obj in self.fields:
                    obj.configure(state=DISABLED)
                try:
                    self.buf = self.clientSocket.recv(26)
                except socket.error:
                    for obj in self.fields:
                        obj.configure(state=DISABLED)
                    self.label.config(text="Connection lost")
                    while True:
                        pass
                self.exmove = int(self.buf.decode('ascii'))
                del self.buf
                self.board[self.exmove] = -1
                self.fields[self.exmove].config(text="O")
                if win(self.board) != 0 or 0 not in self.board:
                    break
            for obj in self.fields:
                obj.configure(state=DISABLED)
            if win(self.board) == 1:
                self.label.config(text="You won")
            elif win(self.board) == 0:
                self.label.config(text="Draw")
            elif win(self.board) == -1:
                self.label.config(text="You lost")
            time.sleep(1)
            self.label.config(text="Restarting")
            time.sleep(1)
            for obj in self.fields:
                obj.config(text="")


class DialogApp(object):
    def __init__(self, master):
        self.droot = master
        self.droot.resizable(False, False)
        self.droot.title("ttt")
        self.droot.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.content = ttk.Frame(self.droot)
        self.label = Label(self.content, text="Choose:")
        self.b1 = Button(self.content, text="Client", width=16, height=2, command=lambda: self.choose(0))
        self.b2 = Button(self.content, text="Server", width=16, height=2, command=lambda: self.choose(1))
        self.content.grid(column=0, row=0)
        self.label.grid(row=0, columnspan=2)
        self.b1.grid(column=0, row=1)
        self.b2.grid(column=1, row=1)

    def on_closing(self):
        self.droot.destroy()
        exit()

    def choose(self, cid):
        self.root = Tk()
        if cid == 0:
            self.app = ClientApp(self.root)
        if cid == 1:
            self.app = ServerApp(self.root)
        self.droot.destroy()
        self.root.mainloop()


root = Tk()
app = DialogApp(root)
root.mainloop()