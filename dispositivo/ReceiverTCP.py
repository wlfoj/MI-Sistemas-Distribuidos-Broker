import socket
import json

from Device import Sensor

def executor(dispositivo: Sensor , comando: str):
    '''FUnção que executa a ação determinada para cada comando'''
    match comando:
        case "Pausar":
            dispositivo.pausar()
        case "Ligar":
            dispositivo.ligar()
        case "Desligar":
            dispositivo.desligar()
        case "Continuar":
            dispositivo.resume()
        case _:
            pass


def Receiver(dispositivo: Sensor, socket: socket.socket):
    '''Função para ser usada como thread para ficar sempre esperando o Broker mandar comandos via tcp.
        Fico esperando o comando chegar. Ao chegar, analiso se possui o campo 'comando' e verifico qual ação tomar para cada comando
    '''
    while 1:
        # Fica aguardando um comando chegar via tcp
        dados_recebidos = socket.recv(1024).decode('utf-8')
        ## Etapa para desserializar 
        dados_recebidos = dados_recebidos.decode('utf-8')
        dados_recebidos = json.loads(dados_recebidos)
        try:
            # Faz validação
            comando = dados_recebidos['comando']
            # Executa a instrução
            executor(dispositivo, comando)
        except:
            continue
    socket.close()
