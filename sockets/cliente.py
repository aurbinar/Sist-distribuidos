import socket
import threading

def receive_messages(client_socket):
    while True:
        # Esperar a recibir datos del servidor
        data = client_socket.recv(1024).decode('utf-8')
        print(data)

# Configuración del cliente
host = '127.0.0.1'  # Dirección IP del servidor
port = 12345  # Puerto del servidor

# Crear un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Iniciar un hilo para recibir mensajes del servidor
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Enviar mensajes al servidor
while True:
    message = input()
    client_socket.send(message.encode('utf-8'))
