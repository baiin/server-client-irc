from queue import Queue
from tkinter import *
import threading
import socket

def send_to_server(message, server_ip, server_port, chat_listbox, chat_input):
    message_bundle = user_name + '\n' + message
    
    if connected == True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(message_bundle.encode(),(server_ip, server_port))
        string_value = "ME: " + message
        chat_listbox.insert(END, string_value)
        chat_listbox.see(END)
        chat_input.delete(0, 'end')
        client_socket.close()
    else:
        chat_listbox.insert(END, "no connection")

def check_connection(listbox):
    while True:
        if connected == True:
            listbox.insert(END, "connection established")
            break

def layout():
    root = Tk()

    root.minsize(300, 400)
    root.maxsize(400, 600)
    root.title(user_name)
        
    chat_listbox = Listbox(root)
    chat_scrollbar = Scrollbar(root)
    chat_input = Entry(root)
    chat_send = Button(root, text="send", command=lambda:send_to_server(chat_input.get(), server_ip, server_port, chat_listbox, chat_input))
            
    chat_listbox.pack(fill=BOTH, expand=TRUE)
    chat_scrollbar.pack(side=RIGHT, in_=chat_listbox, fill=Y)
    chat_input.pack(fill=X)
    chat_send.pack(side=BOTTOM, fill=X)

    chat_listbox.config(yscrollcommand=chat_scrollbar.set)
    chat_scrollbar.config(command=chat_listbox.yview)

    chat_listbox.insert(END, "waiting for connection . . .")

    chat_input.bind('<Return>', lambda _:send_to_server(chat_input.get(), server_ip, server_port, chat_listbox, chat_input))

    thread_var = threading.Thread(target=check_connection, args=(chat_listbox,))
    thread_var.daemon = True
    thread_var.start()

    root.mainloop()

    thread_var.join()
    root.destroy()

def store_user_name(root, entered_name):
    global user_name
    
    if entered_name is "":
        user_name = "anonymous"
    else:
        user_name = entered_name

    root.quit()

def get_user_name():
    root = Tk()

    root.minsize(200, 60)
    root.maxsize(200, 60)
    root.title("user name")

    label_one = Label(root, text="enter a user name")
    entry_one = Entry(root)
    button_one = Button(root, text="submit", command=lambda:store_user_name(root, entry_one.get()))
    entry_one.bind('<Return>', lambda _:store_user_name(root, entry_one.get()))

    label_one.pack(fill=X)
    entry_one.pack(fill=X)
    button_one.pack(fill=X)

    root.mainloop()
    root.destroy()

broadcast_port = 7777
server_ip = ""
server_port = 0

broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
broadcast_socket.bind(('', broadcast_port))

get_user_name()

thread_var = threading.Thread(target=layout)
thread_var.daemon = True
thread_var.start()
connected = False

server_port, server_address = broadcast_socket.recvfrom(2048)

server_ip, server_po = server_address
server_port = int(server_port)
token = True
connected = True


broadcast_socket.close()
thread_var.join()

