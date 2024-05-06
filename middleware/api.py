# Imports referentes ao Flask 
from flask import Flask, request, jsonify
from flask_caching import Cache
# 
import socket
import threading
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






## ============================== BLOCO PARA ENDPOINTS DA API ============================== ##
@app.route('/', methods=['GET'])
def health():
    '''Este endpoint serve apenas para verificar se a API está rodando'''
    return 'HELLO WORLD'


@app.route('/pub/<string:topic>', methods=['POST'])
def post_mensagem(topic: str):
    '''Publica a mensagem no topico. Por estar exposta apenas ao cliente aplicação, só possível fazer postagens de comandos.
    '''
    # Se não for um tópico permitido, já encerra e retorna o status
    if not topic.startswith('command'):
        return jsonify({"erro": "Você não tem permissão para este topico"}), 403
    # Obtem o body da requisição
    conteudo = request.json
    # Verifica se a solicitação contém um JSON
    if conteudo is None:
        return jsonify({"erro": "A solicitação deve conter um JSON"}), 400
    confirm = broker.publish_message(topic, conteudo['message'], '')
    status = 201
    msg = "Mensagem publicada com sucesso"
    if not confirm:
        status = 200
        msg = "Recebemos a solicitação, mas não conseguimos processar"
    return jsonify({"mensagem": msg}), status


@app.route('/sub', methods=['GET'])
@cache.cached(timeout=5)  # Cache válido por 5 segundos
def get_mensagens():
    '''Pega mensagens de todos os tópicos'''
    # Aqui você pode implementar a lógica para ler as mensagens do tópico MQTT
    # Neste exemplo, retornaremos uma lista vazia
    resp = { "data": broker.get_data_from_all_devices()}
    return jsonify(resp), 200



@app.route('/device_names', methods=['GET'])
@cache.cached(timeout=2) # Cache válido por 2 segundos
def get_devices():
    '''Obtem os nomes dos dispositivos com conexões ativas no Broker
    Return.
        - A lista com o nome de dispositivos conetados ao Broker
            EX: ['Dispositivo_1', 'Dispositivo_2']
    '''
    resp = { "data": broker.get_registered_devices()}
    return jsonify(resp), 200








if __name__ == '__main__':
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    origem = (conf['tcp_addres_con'], conf['udp_port'])
    udp.bind(origem)

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    origem = (conf['tcp_addres_con'], conf['tcp_port'])
    tcp.bind(origem)
    tcp.listen(broker._LIMIT_DISP_CONNCTED) ## DEIXEI UM NÚMERO FIXO DE DISPOSITIVOS PARA SE CONECTAREM AQUI

    
    #
    thread_udp = threading.Thread(target=thread_udp_receiver, args=[udp, broker])
    thread_listen_tcp = threading.Thread(target=thread_listen_conections_tcp, args=[tcp, broker])
    thread_send_tcp = threading.Thread(target=thread_send_message, args=[broker])
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

