# Código para envio udp 
import socket
import json

from Device import Sensor, Status
from config import conf

def Sender(dispositivo: Sensor, socket: socket.socket):
    '''Função para ser usada como thread para ficar sempre enviando dados para o Broker via UDP.
        Se o dispositivo estiver ligado, fico enviando dados via udp pro broker. Faço a leitura, coloco no json, serializo e envio.
    '''
    while 1:
        # Só faz envio UDP se o dispositivo estiver ligado
        if dispositivo.obter_status() == Status.On:
            # Lê os dados da estrutura
            dado = dispositivo.ler_dados()
            # Monta a estrutura de envio
            envio = {
                "dado": dado,
            }
            # Serializa o dicionário para JSON
            envio_json = json.dumps(envio).encode('utf-8')
            # Envia os dados para o broker
            socket.sendto(envio_json, (conf['broker_host_ip'], conf['broker_host_port_udp']))
    socket.close()

