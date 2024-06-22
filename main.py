# The 'socket' module in python defines how server and client machines 
# communicates using socket on top of the operating system, at a hardware level. 

# However, the Flask framework is built on top of socket module 
# Flask is a higher level web framework that simplifies the process 
# of building web applications and APIs, it is much easier to handle 
# HTTP requests and responses using Flask. 

# However, flask is not a multi-threaded server that is why Flask is deployed 
# behind a WSGI (Web Server Gateway Interface) server like Gunicorn, uWSGI etc. 
# So, while Flask doesn't handle multi-threading, it can run concurrently and 
# handle multiple requests simultaneously using WSGI. 

# In this application instead of using Flask I'll be using socket and threading 
# A simple Python server that listens on a specified host and port 
# and it uses threading to handle multiple client connections concurrently. 
import socket 
import threading 

# We'll need a host and port to listen on 
# To listen to all available networks use 0.0.0.0
# To listen to my own localhost use 127.0.0.1
# Utilizing client_socket.send() and client_socket.close() methods
# client_socket.recv(1024) to receive data from client in chunks of up to 1024 bytes. 


HOST = '127.0.0.1'
PORT = 8080

def handle_requests(client_socket):
    # To receive data from client 
    receive_data = client_socket.recv(1024)
    if not receive_data:
        return
    
    # A simple response to act as response if there is no data to receive
    # b""  is an empty byte string, it also effectively closes the connection 
    # HTTP status line HTTP/1.1 200 OK
    response_data = b"HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nHello, World!"

    # Sending response to client 
    client_socket.send(response_data)

    # Closing the client socket 
    client_socket.close()

def main(): 
    # The socket object is created in main
    # socket.AF_INET specifies that this is an IPv4 socket,
    # and socket.SOCK_STREAM indicates that this is a TCP socket.

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # A try catch method with exceptin handling 
    try:
        # First we'll need to bind the socket to the host and port 
        server_socket.bind((HOST, PORT))
        # Then listen for the incoming connections up to 5 connections 
        server_socket.listen(5)
        print(f"Listening on {HOST}:{PORT}...")

        while True:
            # Accepting the incoming connections 
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            # New thread to handle request 
            client_thread = threading.Thread(target=handle_requests, args=(client_socket,))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # To close the server socket 
        server_socket.close()

if __name__ == "__main__":
    main()