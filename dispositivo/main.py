import socket
import threading
#
from config import conf
#
from Device import Sensor
# Funções para threads
from interface import MenuPrincipal
from SenderUDP import Sender
from ReceiverTCP import Receiver

###### =========== BLOCO DE CRIAÇÃO DOS SOCKETS =========== ######
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Tenta a conexãoo TCP
socket_tcp.connect((conf['broker_host_ip'], conf['broker_host_port_tcp']))

## INICIALIZADOR DO DISPOSITIVO ##
dispositivo = Sensor("Meu dispositivo", 25)


###### =========== BLOCO DE CRIAÇÃO DA THREADS =========== ######
# == Controle de quando enviar dados via UDP == ##
thread_udp = threading.Thread(target=Sender, args=[dispositivo, socket_udp])
# == Controle para quando receber os comandos via TCP == ##
#thread_tcp = threading.Thread(target=Receiver, args=[dispositivo, socket_tcp])
## == Inicia o controle do menu (interface do dispositivo) == ##
thread_interface_manual = threading.Thread(target=MenuPrincipal, args=[dispositivo])
## Dá start nas threads
thread_interface_manual.start()
thread_udp.start()
#thread_tcp.start()
# Pro caso de dar erro???
thread_udp.join()
thread_interface_manual.join()
#thread_tcp.join()
