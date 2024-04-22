from flask import Flask, request, jsonify

import queue
import threading

from broker import Broker

class FILA():
    def __init__(self, maxsize) -> None:
        self.fila = queue.Queue(maxsize=maxsize)
        self.semaphore = threading.Semaphore(1)  # Defina o valor máximo de threads conforme necessário

    # Função para adicionar elementos à fila com controle de semáforo
    def adicionar_elemento(self, elemento):
        self.semaphore.acquire()  # Adquire o semáforo antes de adicionar o elemento
        self.fila.put(elemento)
        self.semaphore.release()  # Libera o semáforo após adicionar o elemento

    # Função para remover elementos da fila com controle de semáforo
    def remover_elemento(self):
        self.semaphore.acquire()  # Adquire o semáforo antes de remover o elemento
        elemento = self.fila.get()
        self.semaphore.release()  # Libera o semáforo após remover o elemento
        return elemento
    
    
app = Flask(__name__)



def inicializa_topicos():
    topicos_comandos = [{'topic': 'comando_1', 'values': FILA(8)}, {'topic': 'comando_2', 'values': FILA(8)}, 
            {'topic': 'comando_3', 'values': FILA(8)}, {'topic': 'comando_4', 'values': FILA(8)}, 
            {'topic': 'comando_5', 'values': FILA(8)}, {'topic': 'comando_6', 'values': FILA(8)},
            {'topic': 'comando_7', 'values': FILA(8)}, {'topic': 'comando_8', 'values': FILA(8)}]
    
    topicos_dados = [{'topic': 'dados_1', 'values': FILA(32)}, {'topic': 'dados_2', 'values': FILA(32)}, 
            {'topic': 'dados_3', 'values': FILA(32)}, {'topic': 'dados_4', 'values': FILA(32)}, 
            {'topic': 'dados_5', 'values': FILA(32)}, {'topic': 'dados_6', 'values': FILA(32)},
            {'topic': 'dados_7', 'values': FILA(32)}, {'topic': 'dados_8', 'values': FILA(32)}]
    
    return topicos_comandos + topicos_dados


# Rota para publicar uma mensagem no tópico MQTT via método POST
@app.route('/pub', methods=['POST'])
def post_mensagem():
    # Obtem o body da requisição
    conteudo = request.json
    print(conteudo)
    ## === Bloco para validar o body === ##
    # Verifica se a solicitação contém um JSON
    if conteudo is None:
        return jsonify({"erro": "A solicitação deve conter um JSON"}), 400
    # Verifica se os campos num_dispositivo e comando estão presentes no JSON
    #if 'num_dispositivo' not in conteudo or 'comando' not in conteudo:
    #    return jsonify({"erro": "O JSON deve conter os campos 'num_dispositivo' e 'comando'"}), 400
    
    #mensagem = conteudo['mensagem']
    return jsonify({"mensagem": "Mensagem publicada com sucesso"}), 201

# Rota para ler todas as mensagens do tópico MQTT via método GET
@app.route('/mensagens', methods=['GET'])
def get_mensagens():
    # Aqui você pode implementar a lógica para ler as mensagens do tópico MQTT
    # Neste exemplo, retornaremos uma lista vazia
    return jsonify([]), 200

# Rota para ler todas as mensagens do tópico MQTT via método GET
@app.route('/device_names', methods=['GET'])
def get_devices():
    return jsonify(broker.get_devices_allowed()), 200

# Rota para substituir todas as mensagens do tópico MQTT via método PUT
@app.route('/mensagens', methods=['PUT'])
def put_mensagens():
    # Aqui você pode implementar a lógica para substituir todas as mensagens do tópico MQTT
    # Neste exemplo, não faremos nada
    return jsonify({"mensagem": "Operação PUT concluída"}), 200

if __name__ == '__main__':
    broker = Broker()
    app.run(debug=True)
