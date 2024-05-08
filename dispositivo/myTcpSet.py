from Device import Sensor, Status
from Utils import Utils

import socket
from config import conf

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_connect_to_broker():
    '''Procedimento responsável pela conexão com o broker, realizo a conexão e envio um pacote via tcp com a chave de autenticação, caso
    seja recusada, encerro o programa'''
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Faço a conexão
    socket_tcp.connect((conf['broker_host_ip'], conf['broker_host_port_tcp']))
    socket_tcp.settimeout(2)
    logging.info(f'TCP CONN - Conexão realizada com BROKER')
    ## 
    dado = {'key': conf['key_conn']}
    # Criptografa o envio
    dado_criptografado = Utils.encrypt(dado)
    # Envia os dados (chave de autenticação) para o broker
    socket_tcp.sendto(dado_criptografado, (conf['broker_host_ip'], conf['broker_host_port_udp']))
    # Espero o servidor me informar se consegui ser cadastrado
    data_received = socket_tcp.recv(1024)
    #InvalidToken
    msg_decrypted = Utils.decrypt(data_received)
    # Caso o status mostre que não consegui ser cadastrado, encerro o programa
    if msg_decrypted['is_acc'] == False:
        logging.critical(f'TCP CONN - Conexão recusada com BROKER')
        socket_tcp.close()
        socket_tcp = None
    logging.info(f'TCP CONN - Conexão validada e aceita por BROKER')
    return socket_tcp


def try_conn_to_broker(device: Sensor) -> socket.socket:
    conn = False
    device.set_is_conn_with_broker(False)
    # Fico preso no loop até conseguir criar uma nova conexão
    while conn == False:
        try:
            logging.info(f'CONN TCP - Iniciando tentativa de conexão com o Broker')
            socket = create_connect_to_broker()
            if socket == None:
                raise Exception
            conn = True
            device.set_is_conn_with_broker(True)
        except Exception as e:
            logging.info(f'CONN TCP - Tentativa de conexão falhou')
            pass
    logging.info(f'CONN TCP - Conexão com Broker estabelecida')
    return socket


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


def receiverCommandTcp(device: Sensor, socket: socket.socket):
    '''Função para ser usada como thread para ficar sempre esperando o Broker mandar comandos via tcp.
        Fico esperando o comando chegar. Ao chegar, analiso se possui o campo 'comando' e verifico qual ação tomar para cada comando.
        ********OBS. Como eu só me conecto com o broker, não preciso verificar a coerência da mensagem recebida.
    '''
    # logging.info(f'TCP - Thread ouvinte de comandos do Broker na porta TCP iniciada')
    while 1:
        # Fica aguardando um comando chegar via tcp
        try:
            data_received = socket.recv(1024)
            if data_received == None:
                raise Exception
        except:
            # Se tiver erro ou não chegar nada, significa que um cabo foi desconectado
            socket.close()
            socket = try_conn_to_broker(device)
            continue
        # Se recbi algum dado
        if data_received:
            # Etapa de tirar criptografia
            try:
                msg_decrypted = Utils.decrypt(data_received)
                logging.info(f'TCP - Pacote recebido -> {msg_decrypted}')
                # Faz validação
                command = msg_decrypted['command']
                if command == 'ping':
                    obj_to_send = {'command': 'ping'}
                    # Criptografa
                    obj_encrypted = Utils.encrypt(obj_to_send)
                    # Envia
                    try:
                        socket.send(obj_encrypted) # Envio a mensagem para a conexão correspondente
                    except:
                        socket.close()
                        socket = try_conn_to_broker(device)
                    continue
                # Executa a instrução
                executor(device, command)
            except:
                # Se cair algum comando defeituoso eu ignoro
                pass
    socket.close()

