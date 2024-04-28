# Código para envio udp 
from Device import Sensor, Status
from Utils import Utils
from config import conf

import socket
import time
from cryptography.fernet import Fernet


def senderDataUdp(device: Sensor, socket: socket.socket, encrypt: Fernet):
    '''Função para ser usada como thread para ficar sempre enviando dados para o Broker via UDP.
        Se o dispositivo estiver ligado, fico enviando dados via udp pro broker. Faço a leitura, coloco no json, serializo e envio.
    '''
    while 1:
        # Só faz envio UDP se o dispositivo estiver ligado
        if device.get_status() == Status.On:
            # Lê os dados da estrutura
            data = device.get_data()
            # Monta a estrutura de envio
            json_data = {
                "data": data,
            }
            print('Vou enviar UDP:', json_data)
            # Criptografa os dados
            data_crypted = Utils.encrypt(encrypt, json_data)
            # Envia os dados para o broker
            socket.sendto(data_crypted, (conf['broker_host_ip'], conf['broker_host_port_udp']))
            time.sleep(1.5)
    socket.close()


