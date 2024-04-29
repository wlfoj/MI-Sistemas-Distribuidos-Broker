from Device import Sensor, Status
from Utils import Utils

import socket
import sys
from cryptography.fernet import Fernet

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    while 1:
        # Fica aguardando um comando chegar via tcp
        try:
            data_received = socket.recv(1024)
        except ConnectionResetError:
            logging.critical(f'TCP - Conexão com BROKER foi perdida. A Thread que escuta mensagens TCP será encerrada e a aplicação deve ser reiniciada.')
            break
            
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
