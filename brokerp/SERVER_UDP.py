import socket

from broker import Broker


def thread_receiva_udp(udp_socket: socket.socket, broker: Broker):
    '''Esta função atua apenas ouvindo conexões e registrando no broker'''
    print("inicei a thread upd")
    # Loop infinito para receber mensagens
    while True:
        #
        # Recebe uma mensagem e o endereço do cliente
        mensagem, endereco_cliente = udp_socket.recvfrom(1024)
        print(mensagem)
        # # Converte a mensagem de bytes para string
        # mensagem_decodificada = mensagem.decode('utf-8')
        # topic = broker.get_topic_to_ip(endereco_cliente[0])

        # broker.publish_message(topic, mensagem_decodificada, endereco_cliente[0])
        #print(broker.topico)

