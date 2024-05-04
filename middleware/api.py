# Imports referentes ao Flask 
from flask import Flask, request, jsonify
from flask_caching import Cache
# 
import socket
import threading
from cryptography.fernet import Fernet
# Imports referentes ao broker e ao de mensagens via TCP e UDP
from SERVER_TCP import thread_listen_conections_tcp, thread_send_message, thread_check_conn_health
from SERVER_UDP import thread_udp_receiver
from config import conf
from Broker import Broker
#
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

## ======= Bloco para instânciação de objetos necessários ======= ##
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  # Configuração básica de cache
broker = Broker()
fernet = Fernet(conf['key_decrypt']) 









## ========== Bloco para os endpoints da API ========== ##
@app.route('/pub/<string:topic>', methods=['POST'])
def post_mensagem(topic: str):
    '''Publica a mensagem no topico'''
    # Se não for um tópico permitido, já encerra e retorna o status
    if not topic.startswith('command'):
        return jsonify({"erro": "Você não tem permissão para este topico"}), 403
    # Obtem o body da requisição
    conteudo = request.json
    # print(conteudo['topico'])
    ## === Bloco para validar o body === ##
    # Verifica se a solicitação contém um JSON
    if conteudo is None:
        return jsonify({"erro": "A solicitação deve conter um JSON"}), 400
    confirm = broker.publish_message(topic, conteudo['message'], '')
    status = 200
    if confirm:
        status = 201
    return jsonify({"mensagem": "Mensagem publicada com sucesso"}), status



@app.route('/', methods=['GET'])
def hello():
    return 'HELLO WORLD'

@app.route('/sub', methods=['GET'])
@cache.cached(timeout=5)  # Cache válido por 5 segundos
def get_mensagens():
    '''Pega mensagens de todos os tópicos'''
    # Aqui você pode implementar a lógica para ler as mensagens do tópico MQTT
    # Neste exemplo, retornaremos uma lista vazia
    return jsonify(broker.get_data_from_all_devices()), 200


# Rota para ler as mensagens de um dispositivo especifico
@app.route('/sub/<string:topic>', methods=['GET'])
@cache.cached(timeout=5)  # Cache válido por 5 segundos
def get_mensagem(topic:str):
    '''Pega uma mensagem de um topico'''
    # Se não for um tópico permitido, já encerra e retorna o status
    if not topic.startswith('data_'):
        return jsonify({"erro": "Você não tem permissão para este topico"}), 403
    msg = broker.pop_message(topic)
    # Aqui você pode implementar a lógica para ler as mensagens do tópico MQTT
    # Neste exemplo, retornaremos uma lista vazia
    return jsonify({'value': msg}), 200


@app.route('/device_names', methods=['GET'])
@cache.cached(timeout=2)  # Cache válido por 5 segundos
def get_devices():
    '''Obtem os nomes dos dispositivos cadastrados'''
    return jsonify(broker.get_registered_devices()), 200








if __name__ == '__main__':
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    origem = (conf['tcp_addres_con'], conf['udp_port'])
    udp.bind(origem)

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    origem = (conf['tcp_addres_con'], conf['tcp_port'])
    tcp.bind(origem)
    tcp.listen(broker._LIMIT_DISP_CONNCTED) ## DEIXEI UM NÚMERO FIXO DE DISPOSITIVOS PARA SE CONECTAREM AQUI

    
    #
    thread_udp = threading.Thread(target=thread_udp_receiver, args=[udp, broker, fernet])
    thread_listen_tcp = threading.Thread(target=thread_listen_conections_tcp, args=[tcp, broker, fernet])
    thread_send_tcp = threading.Thread(target=thread_send_message, args=[broker, fernet])
    thread_health_tcp = threading.Thread(target=thread_check_conn_health, args=[broker])
    ## Dá start nas threads 
    thread_listen_tcp.start()
    thread_udp.start()
    thread_send_tcp.start()
    thread_health_tcp.start()
    #

    # Pro caso de dar erro???
    # Dou start nas threads udp e tcp
    # Dou start na thread de processamento
    # Dou start na thread do broker????
    # Dou start no api restful
    app.run(port=5005, host='0.0.0.0')

    thread_listen_tcp.join()
    thread_udp.join()
    thread_send_tcp.join()
    thread_health_tcp.join()

