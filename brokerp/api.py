from flask import Flask, request, jsonify

from broker import Broker

app = Flask(__name__)
broker = Broker(1)



@app.route('/pub/<string:topic>', methods=['POST'])
def post_mensagem(topic: str):
    '''Publica a mensagem no topico'''
    # Se não for um tópico permitido, já encerra e retorna o status
    if not topic.startswith('comandos_'):
        return jsonify({"erro": "Você não tem permissão para este topico"}), 403
    # Obtem o body da requisição
    conteudo = request.json
    # print(conteudo['topico'])
    ## === Bloco para validar o body === ##
    # Verifica se a solicitação contém um JSON
    if conteudo is None:
        return jsonify({"erro": "A solicitação deve conter um JSON"}), 400
    confirm = broker.publish_message(topic, conteudo, '')
    status = 200
    if confirm:
        status = 201
    return jsonify({"mensagem": "Mensagem publicada com sucesso"}), status

@app.route('/sub', methods=['GET'])
def get_mensagens():
    '''Pega mensagens de todos os tópicos'''
    # Aqui você pode implementar a lógica para ler as mensagens do tópico MQTT
    # Neste exemplo, retornaremos uma lista vazia
    return jsonify(broker.pega_mensagens_todos_topicos_dados()), 200


# Rota para ler as mensagens de um dispositivo especifico
@app.route('/sub/<string:topic>', methods=['GET'])
def get_mensagem(topic:str):
    '''Pega uma mensagem de um topico'''
    # Se não for um tópico permitido, já encerra e retorna o status
    if not topic.startswith('dados_'):
        return jsonify({"erro": "Você não tem permissão para este topico"}), 403
    msg = broker.pop_message(topic)
    # Aqui você pode implementar a lógica para ler as mensagens do tópico MQTT
    # Neste exemplo, retornaremos uma lista vazia
    return jsonify({'value': msg}), 200




@app.route('/device_names', methods=['GET'])
def get_devices():
    '''Obtem os nomes dos dispositivos cadastrados'''
    return jsonify(broker.get_registered_devices()), 200




if __name__ == '__main__':
    
    app.run(debug=True)
