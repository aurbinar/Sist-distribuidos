import socket
import threading

def handle_client(client_socket, client_number):
    try:
        while True:
            # Esperar a recibir datos del cliente
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                # Si no hay datos, se desconectó el cliente
                print(f"Cliente {client_number} desconectado")
                break
            client_data = 'Cliente '+str(client_number)+': '+data
            print(client_data)
            # Enviar los datos recibidos a todos los clientes conectados (incluido el remitente)
            broadcast(client_data,  client_socket)
    except Exception as e:
        print("Excepción:", e)
    finally:
        # Cerrar la conexión con el cliente
        client_socket.close()

def broadcast(message, sender_client):
    # Enviar el mensaje a todos los clientes conectados excepto el remitente
    for client in clients:
        if client[0] != sender_client:
            client[0].send(message.encode('utf-8'))


# Configuración del servidor
host = '127.0.0.1'  # Dirección IP del servidor
port = 12345  # Puerto del servidor

# Crear un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)  # Esperar hasta 5 conexiones entrantes

print('El servidor está listo para recibir conexiones...')

clients = []  # Lista de clientes conectados
client_number = 1  # Número del cliente


while True:
    # Esperar a que llegue una nueva conexión
    client_socket, addr = server_socket.accept()
    print('Cliente', client_number, 'conectado:', addr)

    # Agregar el nuevo cliente a la lista
    clients.append((client_socket, client_number))

    # Iniciar un nuevo hilo para manejar la comunicación con el cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_number))
    client_thread.start()

    client_number += 1
