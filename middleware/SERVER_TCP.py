import socket
from cryptography.fernet import Fernet
from Broker import Broker
import time
from config import conf

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from Utils import Utils

def thread_listen_conections_tcp(socket_tcp: socket.socket, broker: Broker):
    '''Esta função atua apenas ouvindo conexões e registrando no broker'''
    logging.info(f'TCP LISTEN CONN - Thread para receber conexões na porta tcp iniciada')
    while True:
        # Aceitando uma nova conexão
        conexao, cliente = socket_tcp.accept()
        if conexao and cliente:
            logging.info(f'TCP LISTEN CONN - Conexão recebida de {cliente[0]}')
            ### ================ Valido a conexão ================ ###
            ## Devo receber, logo após aceitar uma conexão, um dado no tipo {'key': "valor_da_secret"} 
            dados_recebidos = conexao.recv(1024)
            logging.info(f'TCP LISTEN CONN - mensagem para validar a conexão recebida de {cliente[0]}')
            # O try existe para o caso de dar algum erro no decriptar
            try:
                # decodifica
                mensagem_json_dict = Utils.decrypt(dados_recebidos)
                # ============ Valido a conexão ============= #
                if mensagem_json_dict['key'] == conf['key_conn']:
                    # Coloco um timeout aqui para ajudar a 
                    conexao.settimeout(2)
                    # Registra o cliente no broker
                    confirm = broker.register_device(conexao, cliente[0])
                    if confirm:
                        logging.info(f'TCP LISTEN CONN - Conexão aceita de {cliente[0]} e registrada no BROKER')
                        # Envio a confirmação
                                            # Monta o obj
                        obj_to_send = {'is_acc': True}
                        # Criptografa
                        obj_encrypted = Utils.encrypt(obj_to_send)
                        # Envia
                        conexao.send(obj_encrypted)
                        #print(broker._dispositivos)
                    else:
                        logging.warning(f'TCP LISTEN CONN - Conexão de {cliente[0]} rejeitada pelo BROKER')
                        conexao.close()
                else:
                    obj_to_send = {'is_acc': False}
                    # Criptografa
                    obj_encrypted = Utils.encrypt(obj_to_send)
                    # Envia
                    conexao.send(obj_encrypted)
                    logging.warning(f'TCP LISTEN CONN - Conexão de {cliente[0]} rejeitada, pois a chave está incorreta')
                    conexao.close()
            except:
                obj_to_send = {'is_acc': False}
                # Criptografa
                obj_encrypted = Utils.encrypt(obj_to_send)
                # Envia
                conexao.send(obj_encrypted)
                logging.warning(f'TCP LISTEN CONN - Conexão de {cliente[0]} rejeitada, pois a chave está incorreta')
                conexao.close()
 


def thread_send_message(broker: Broker):
    '''Função responsável por repassar o comando no tópico para o respectivo dispositivo
    '''
    logging.info(f'TCP - Thread para enviar mensagens pela porta tcp iniciada')
    while True:
        # Percoro os tópicos de comandos vendo quais tem mensagens para serem mandadas
        to_send = broker.get_msg_and_device_to_send_command()
        # Percorrendo a lista de operações que preciso fazer
        for info in to_send:
            # Faço o envio
            if (info['msg'] is not None) :#and (info['conn'] is not None):
                try:
                    msg = info['msg']
                    ip = info['ip']
                    logging.info(f'TCP - Enviando {msg} para {ip} via tcp')
                    # Monta o obj
                    obj_to_send = {'command': msg}
                    # Criptografa
                    obj_encrypted = Utils.encrypt(obj_to_send)
                    # Envia
                    info['conn'].send(obj_encrypted) # Envio a mensagem para a conexão correspondente
                except ConnectionResetError:
                    info['conn'].close()
                    broker.delete_device(ip)
                    logging.warning(f'TCP - O dispositivo {ip} foi desconectado e por isso removido do broker')




def thread_check_conn_health(broker: Broker):
    '''Thread para verificar se uma conexão está ativa e destruir ela se não estiver'''
    logging.info(f'TCP HEALTH CONN - Thread para verificar a saúde das conexões iniciada')
    #{"device_name":"", "ip": '', "tcp_connection": None}
    while True:
        time.sleep(1) # Repito o processo de 1 em 1 segundo
        for device in broker.get_devices():
            msg = {"command": 'ping'}
            msg_crypt = Utils.encrypt(msg)
            try:
                logging.info(f"TCP HEALTH CONN - Testando a conexão do device {device['ip']}")
                # Tenta enviar uma especie de ping que será desconsiderado peo dispositivo, apenas para verificar se ainda está conectado
                device['tcp_connection'].send(msg_crypt)
                # E espero ter qualquer resposta
                response = device['tcp_connection'].recv(1024)
                # Se n  tiver, é pq retiraram o cabo, se der alguma exceção também
                if not response:
                    broker.delete_device(device['ip'])
                    logging.warning(f"TCP HEALTH CONN - O dispositivo {device['ip']} foi desconectado e por isso removido do broker") 
            except:
                # Se ocorrer um erro no envio, estou supondo que a conexão não está mais ativa
                broker.delete_device(device['ip'])
                logging.warning(f"TCP HEALTH CONN - O dispositivo {device['ip']} foi desconectado e por isso removido do broker") 