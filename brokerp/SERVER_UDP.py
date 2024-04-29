import socket
from Utils import Utils
from cryptography.fernet import Fernet
from broker import Broker

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def thread_udp_receiver(udp_socket: socket.socket, broker: Broker, decrypt: Fernet):
    '''Esta função atua apenas recebendo os envios UDP e publicando no broker no tópico permitido para determinado IPv4'''
    # Loop infinito para receber mensagens
    logging.info(f'UDP - Thread para receber dados via porta udp iniciada')
    while True:
        # Recebe uma mensagem e o endereço do cliente
        mensagem, client_addr = udp_socket.recvfrom(1024)
        # # Decodifica a mensagem
        mensagem_json_dict = Utils.decrypt(decrypt, mensagem)
        logging.info(f'UDP - Mensagem de {client_addr[0]} recebida na porta udp -> {mensagem_json_dict}')

        #  Obtenho o tópico em que o ip pode publicar
        topic = broker.get_topic_name_publisher_by_ip(client_addr[0])
        # Se tiver algum tópico, faço a publicação
        if topic is not None:
            broker.publish_message(topic, mensagem_json_dict['data'], client_addr[0])
            logging.info(f'UDP - Mensagem de {client_addr[0]} publicada no topico={topic}')
        # Só registro a mensagem no tópico se o dispositivo estiver cadastrado, aí eu vou no tópico equivalente

        # topic = broker.get_topic_to_ip(endereco_cliente[0])

        
        #print(broker.topico)

