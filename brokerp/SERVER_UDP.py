import socket
import json
from cryptography.fernet import Fernet
from broker import Broker


def thread_udp_receiver(udp_socket: socket.socket, broker: Broker, decrypt: Fernet):
    '''Esta função atua apenas recebendo os envios UDP e publicando no broker no tópico permitido para determinado IPv4'''
    # Loop infinito para receber mensagens
    while True:
        # Recebe uma mensagem e o endereço do cliente
        mensagem, client_addr = udp_socket.recvfrom(1024)
        # Decodifica a mensagem
        mensagem_descriptografado = decrypt.decrypt(mensagem)
        # # Converte a mensagem de bytes para string
        mensagem_string = mensagem_descriptografado.decode('utf-8')
        mensagem_json_dict = json.loads(mensagem_string)
        print(f"Recebi UDP {client_addr[0]}: {mensagem_json_dict}")

        #  Obtenho o tópico em que o ip pode publicar
        topic = broker.get_topic_name_publisher_by_ip(client_addr[0])
        # Se tiver algum tópico, faço a publicação
        if topic is not None:
            broker.publish_message(topic, mensagem_json_dict['data'], client_addr[0])
        # Só registro a mensagem no tópico se o dispositivo estiver cadastrado, aí eu vou no tópico equivalente

        # topic = broker.get_topic_to_ip(endereco_cliente[0])

        
        #print(broker.topico)

