import socket


# take a photo from image device
def take_a_photo_from_image_device():
    tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象
    host = "169.254.91.18"  # socket.gethostname()
    port = 50000  # port
    # get address
    addr = (host, port)
    # connect server
    tcpClient.connect(addr)  # connection service, set host and port
    # take photos of the upper face of the engine
    message1 = 'CCDD33010010001054A8'  # message data，class type: string
    tcpClient.send(message1.encode())  # send message.encode() to server
    receive_data_from_server = tcpClient.recv(1024)  # receive data from server, max bytes: 1024 bytes
    receive_data = receive_data_from_server.decode()
    print("get receive data from server: {}".format(receive_data))
    tcpClient.close()
    return receive_data
