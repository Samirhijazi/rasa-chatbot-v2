import socket
import socket

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8888))  # Connect to the server's IP and port

while True:
    message = input("Enter a message: ")
    if message == "":
        print("Message is empty. Not sending.")
    elif message.lower() == "sleep":
        print("Okay, I'm sleeping.")
        # You can implement a sleep here if needed
    else:
        # Send the message to the server
        client_socket.send(message.encode("utf-8"))
        
        # Receive and print the response from the server
        response = client_socket.recv(1024).decode("utf-8")
        print("Server response:", response)

# Close the socket when done
client_socket.close()