import socket
from cryptography.fernet import Fernet
from broker import Broker
import json
from config import conf

from Utils import Utils

def thread_listen_conections_tcp(socket_tcp: socket.socket, broker: Broker, decrypt: Fernet):
    '''Esta função atua apenas ouvindo conexões e registrando no broker'''
    while True:
        # Aceitando uma nova conexão
        conexao, cliente = socket_tcp.accept()
        if conexao and cliente:
            ### ================ Valido a conexão ================ ###
            ## Devo receber, logo após aceitar uma conexão, um dado no tipo {'key': "valor_da_secret"} 
            dados_recebidos = conexao.recv(1024)
            # Decodifica a mensagem
            mensagem_descriptografado = decrypt.decrypt(dados_recebidos)
            # # Converte a mensagem de bytes para string
            mensagem_string = mensagem_descriptografado.decode('utf-8')
            mensagem_json_dict = json.loads(mensagem_string)
            # ============ Valido a conexão ============= #
            if mensagem_json_dict['key'] == conf['key_conn']:
                # Registra o cliente no broker
                broker.register_device(conexao, cliente[0])
                # Envio a confirmação
                                    # Monta o obj
                obj_to_send = {'is_acc': True}
                # Criptografa
                obj_encrypted = Utils.encrypt(decrypt, obj_to_send)
                # Envia
                conexao.send(obj_encrypted)
                #print(broker._dispositivos)
            else:
                obj_to_send = {'is_acc': False}
                # Criptografa
                obj_encrypted = Utils.encrypt(decrypt, obj_to_send)
                # Envia
                conexao.send(obj_encrypted)
                print("Conexão negada")
                conexao.close()


def thread_send_message(broker: Broker, encrypt: Fernet):
    '''Função responsável por repassar o comando no tópico para o respectivo dispositivo
    '''
    while True:
        # Percoro os tópicos de comandos vendo quais tem mensagens para serem mandadas
        to_send = broker.get_msg_and_device_to_send_command()
        # Percorrendo a lista de operações que preciso fazer
        for info in to_send:
            print(f"Vou enviar TCP: {info}")
            # Faço o envio
            if (info['msg'] is not None) and (info['conn'] is not None):
                try:
                    # Monta o obj
                    obj_to_send = {'command': info['msg']}
                    # Criptografa
                    obj_encrypted = Utils.encrypt(encrypt, obj_to_send)
                    # Envia
                    info['conn'].send(obj_encrypted) # Envio a mensagem para a conexão correspondente
                except ConnectionResetError:
                    info['conn'].close()
                    broker.delete_device(info['ip'])




