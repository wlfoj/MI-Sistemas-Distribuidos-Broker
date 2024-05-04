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
from myTcpSet import receiverCommandTcp, try_connect_to_broker

# import logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

## ====================== BLOCO DE FUNÇÕES AUXILIARES ====================== ##
   


## ====================== INICIALIZADOR DO DISPOSITIVO ====================== ##
dispositivo = Sensor("Meu dispositivo", 25, 'F')
fernet = Fernet(conf['key_crypt']) 
###### ====================== BLOCO DE CRIAÇÃO DOS SOCKETS ====================== ######
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

### Tenta a conexão TCP ###
conn = False
while conn == False:
    try:
        # logging.critical(f'TCP - Iniciando a tentativa de conexão com o Broker.')
        socket_tcp = try_connect_to_broker(fernet)
        if socket_tcp == None:
            sys.exit() # Se o token for inválido ou etc, já encerro o device
        conn = True # Mudo a variavel de controle do loop, pois se consegui me conectar já posso prosseguir.
    except:
        conn = False
        socket_tcp.close() # Fecho a conexão para tentar reiniciar
        # logging.critical(f'TCP - Não foi possível estabelecer conexão com o Broker.')


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
