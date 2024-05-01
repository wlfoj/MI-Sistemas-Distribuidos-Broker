from config import conf
from Device import Sensor
from Utils import Utils
#
import socket
import threading
import json
import sys
from cryptography.fernet import Fernet
# Funções para threads
from interface import mainMenu
from myUdpSet import senderDataUdp
from myTcpSet import receiverCommandTcp

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

## ====================== BLOCO DE FUNÇÕES AUXILIARES ====================== ##
def try_connect_to_broker(socket_tcp: socket.socket, fernet: Fernet):
    '''Procedimento responsável pela conexão com o broker, realizo a conexão e envio um pacote via tcp com a chave de autenticação, caso
    seja recusada, encerro o programa'''
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
    print(data_received)
    msg_decrypted = Utils.decrypt(fernet, data_received)
    # Caso o status mostre que não consegui ser cadastrado, encerro o programa
    if msg_decrypted['is_acc'] == False:
        logging.critical(f'Conexão recusada com BROKER')
        sys.exit()
    logging.info(f'Conexão validada e aceita por BROKER')
    


## ====================== INICIALIZADOR DO DISPOSITIVO ====================== ##
dispositivo = Sensor("Meu dispositivo", 25)
fernet = Fernet(conf['key_crypt']) 
###### ====================== BLOCO DE CRIAÇÃO DOS SOCKETS ====================== ######
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
### Tenta a conexão TCP ###
try_connect_to_broker(socket_tcp, fernet)

###### =========== BLOCO DE CRIAÇÃO DA THREADS =========== ######
# == Controle de quando enviar dados via UDP == ##
thread_udp = threading.Thread(target=senderDataUdp, args=[dispositivo, socket_udp, fernet])
thread_udp.daemon = True
# == Controle para quando receber os comandos via TCP == ##
thread_tcp = threading.Thread(target=receiverCommandTcp, args=[dispositivo, socket_tcp, fernet])
thread_tcp.daemon = True
## == Inicia o controle do menu (interface do dispositivo) == ##
thread_interface_manual = threading.Thread(target=mainMenu, args=[dispositivo])
thread_interface_manual.daemon = True

###### Dá start nas threads ######
thread_interface_manual.start()
thread_udp.start()
thread_tcp.start()

###### Pro caso de dar erro ######
thread_udp.join()
thread_interface_manual.join()
thread_tcp.join()
