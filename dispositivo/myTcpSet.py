from Device import Sensor, Status
from Utils import Utils

import socket
import sys
from cryptography.fernet import Fernet
import json
from config import conf

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def try_connect_to_broker(fernet: Fernet):
    '''Procedimento responsável pela conexão com o broker, realizo a conexão e envio um pacote via tcp com a chave de autenticação, caso
    seja recusada, encerro o programa'''
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Faço a conexão
    socket_tcp.connect((conf['broker_host_ip'], conf['broker_host_port_tcp']))
    logging.info(f'Conexão realizada com BROKER')
    ## 
    dado = {'key': conf['key_conn']}
    # Serializa o dicionário para JSON STRING(até dumps) em bytes (encode)
    envio_json = json.dumps(dado).encode('utf-8')
    # Criptografa o envio
    dado_criptografado = fernet.encrypt(envio_json)
    # Envia os dados (chave de autenticação) para o broker
    socket_tcp.sendto(dado_criptografado, (conf['broker_host_ip'], conf['broker_host_port_udp']))
    # Espero o servidor me informar se consegui ser cadastrado
    data_received = socket_tcp.recv(1024)
    #InvalidToken
    msg_decrypted = Utils.decrypt(fernet, data_received)
    # Caso o status mostre que não consegui ser cadastrado, encerro o programa
    if msg_decrypted['is_acc'] == False:
        logging.critical(f'Conexão recusada com BROKER')
        # sys.exit()
        return None
    logging.info(f'Conexão validada e aceita por BROKER')
    return socket_tcp

def executor(device: Sensor , command: str):
    '''Função que executa a ação determinada para cada comando'''
    match command:
        case "Pausar":
            device.set_status(Status.Pause)
        case "Ligar":
            device.set_status(Status.On)
        case "Desligar":
            device.set_status(Status.Off)
        case "Continuar":
            if device.get_status == Status.Pause:
                device.set_status(Status.On)
        case _:
            pass


def receiverCommandTcp(device: Sensor, socket: socket.socket, decrypt: Fernet):
    '''Função para ser usada como thread para ficar sempre esperando o Broker mandar comandos via tcp.
        Fico esperando o comando chegar. Ao chegar, analiso se possui o campo 'comando' e verifico qual ação tomar para cada comando.
        ********OBS. Como eu só me conecto com o broker, não preciso verificar a coerência da mensagem recebida.
    '''
    logging.info(f'TCP - Thread ouvinte de comandos do Broker na porta TCP iniciada')
    conn = True
    while 1:
        # Fica aguardando um comando chegar via tcp
        try:
            data_received = socket.recv(1024)
        except ConnectionResetError:
            socket.close()
            logging.critical(f'TCP - Conexão com BROKER foi perdida. A Thread que escuta mensagens TCP será encerrada e a aplicação deve ser reiniciada.')
            conn = False
            while conn == False:
                logging.info(f'TCP CONN - Iniciando nova tentativa de conexão com o BROKER.')
                try:
                    socket = try_connect_to_broker(decrypt)
                    conn = True
                except Exception as e:
                    print(e)
                    logging.critical(f'TCP CONN - Não foi possível estabelecer conexão com broker.')
            continue
            
        # Se recbi algum dado
        if data_received:
            # Etapa de tirar criptografia
            msg_decrypted = Utils.decrypt(decrypt, data_received)
            logging.info(f'TCP - Pacote recebido -> {msg_decrypted}')
            # Faz validação
            command = msg_decrypted['command']
            # Executa a instrução
            executor(device, command)
    socket.close()
