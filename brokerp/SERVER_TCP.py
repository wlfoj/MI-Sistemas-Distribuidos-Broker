import socket

from broker import Broker

def thread_listen_conections(socket_tcp: socket.socket, broker: Broker):
    '''Esta função atua apenas ouvindo conexões e registrando no broker'''

    while True:
        # Aceitando uma nova conexão
        conexao, cliente = socket_tcp.accept()

        if conexao and cliente:
            # Registra o cliente no broker
            broker.register_device(conexao, cliente[0])


def thread_send_message(broker: Broker):
    '''Função responsável por repassar o comando no tópico para o respectivo dispositivo'''
    while True:
        # Percoro os tópicos de comandos vendo quais tem mensagens para serem mandadas
        # obtenho a mensagem que deve ser passada para o dispositivo
        msg, conn = broker.pega_mensagem_e_ouvinte()
        # Faço o envio
        if (msg is not None) and (conn is not None):
            conn.send(msg) # Envio a mensagem para a conexão correspondente
        