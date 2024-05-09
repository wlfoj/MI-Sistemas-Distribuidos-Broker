from config import conf
from Device import Sensor
#
import socket
import threading
import sys
# Funções para threads
from interface import mainMenu
from myUdpSet import senderDataUdp
from myTcpSet import receiverCommandTcp, try_conn_to_broker

# import logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

## ====================== BLOCO DE FUNÇÕES AUXILIARES ====================== ##
   


## ====================== INICIALIZADOR DO DISPOSITIVO ====================== ##
sensor = Sensor("Meu dispositivo", 25, conf['unit_measurement'])
###### ====================== BLOCO DE CRIAÇÃO DOS SOCKETS ====================== ######
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.settimeout(2)
### =========== Tenta a conexão TCP =========== ###
socket_tcp = try_conn_to_broker(sensor)
if socket_tcp == None:
    sys.exit()
# sensor.set_is_conn_with_broker(True)


###### =========== BLOCO DE CRIAÇÃO DA THREADS =========== ######
# == Controle de quando enviar dados via UDP == ##
thread_udp = threading.Thread(target=senderDataUdp, args=[sensor, socket_udp])
thread_udp.daemon = True
# == Controle para quando receber os comandos via TCP == ##
thread_tcp = threading.Thread(target=receiverCommandTcp, args=[sensor, socket_tcp])
thread_tcp.daemon = True
## == Inicia o controle do menu (interface do sensor) == ##
thread_interface_manual = threading.Thread(target=mainMenu, args=[sensor])
thread_interface_manual.daemon = True

###### Dá start nas threads ######
thread_interface_manual.start()
thread_udp.start()
thread_tcp.start()

###### Pro caso de dar erro ######
thread_udp.join()
thread_interface_manual.join()
thread_tcp.join()
