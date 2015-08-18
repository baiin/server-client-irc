import threading
import tkinter
import socket

def broadcast():
    broadcast_port = 7777
    broadcast_message = str(5555)
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print("sending broadcast . . .")
    broadcast_socket.sendto(broadcast_message.encode(), ('<broadcast>', broadcast_port))
    broadcast_socket.close()

def button():
    root = tkinter.Tk()
    root.minsize(300,300)
    root.geometry("500x500")
    broadcast_button = tkinter.Button(root, text="broadcast", fg="black", command=broadcast)
    broadcast_button.pack()
    root.mainloop()
    root.destroy()

def main():
    server_address = "192.168.0.195"
    server_port = 5555
    
    thread_var = threading.Thread(target = button)
    thread_var.daemon = True
    thread_var.start()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', server_port))
    print("server listening . . .")

    while True:
        data, client_info = server_socket.recvfrom(2048)
        data = data.decode()
        data = data.split('\n')
        client_addr, client_port = client_info
        print(data[0], ": ", data[1])

        if data[1] == "QUIT":
            break

    server_socket.close()
    thread_var.join()


main()
