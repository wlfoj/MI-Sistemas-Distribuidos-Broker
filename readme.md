# 0. Passo a passo para executar no LARSID
É necessário que a Aplicação rode em um computador com [Python](https://www.python.org) 3.11, ou mais recente, instalado. É preciso que o computador tenha o Docker instalado, pois o Broker e os Devices serão executados por  meio de containers.

### 0.1 Faça pull das imagens utilizadas
Abra o terminal e execute os comandos abaixo para baixar as imagens do Broker e do Device no Doocker Hub.
```
$ docker pull wolivej/middleware_b_i:latest
$ docker pull wolivej/device_i:latest
```
### 0.2 Iniciando o Broker
Para que tudo funcione da melhor forma, é necessário iniciar o serviço do Broker antes dos demais. Sendo assim, execute o seguinte comando em um determinado computador.
```
$ docker run --network=host -it -p 5005:5005 wolivej/middleware_b_i:latest
```
Anote o endereço IP do computador em que o Broker está rodando.
### 0.3 Iniciando os Devices
Em um novo terminal, execute o comando, logo abaixo, para criar o serviço do dispositivo e substitua 'ip_do_broker' pelo IP anotado no passo anterior. A variável de ambiente UNIT_MEASUREMENT pode representar qualquer unidade de medida, Coloque uma unidade para cada Device instânciado.
```
$ docker run --network=host -it -e BROKER_IP=ip_do_broker -e UNIT_MEASUREMENT=mV wolivej/device_i:latest
```
Com o container já iniciado, é preciso dar o start no processo do Device. Execute o comando abaixo no container iniciado no código acima.
```
$ python main.py
```
Repita o processo para cada dispositivo que você queira criar.
### 0.3 Iniciando a Aplicação
Por fim, devemos iniciar a aplicação gráfica que irá consumir os dados do Broker. Baixe o arquivo [main.py](https://github.com/wlfoj/concorrencia-conectividade/blob/main/aplicacaoGF/main.py) e execute o comando abaixo, substituindo 'ip_do_broker' pelo IP anotado no passo **0.2**.
```
$ python main.py ip_do_broker
```
Como exemplo:
```
$ python main.py 127.0.0.1
```

# 0. Passo a passo para execução no próprio computador
### 0.1 Criação dos containers
Para criar o sistema de maneira isolada no seu computador, execute o comando abaixo no seu terminal, estando na pasta raiz do projeto. O comando irá criar um container para o Broker e 4 containers para os dispositivos.   
```
$ docker-compose up
```
### 0.2 Iniciando os dispositivos
**Passo 1:** Uma vez criado os containers, não será necessário iniciar o container do Broker, pois o mesmo já estará sendo executado. Entretanto, os dispositivos necessitam serem iniciados manualmente, devido a sua caracteristica interativa. Primeiro obtenha o nome dos containers de cada dispositivo (são todos os iniciados com "concorrencia-conectividade-device") com o  comando abaixo.
```
$ docker ps
```
**Passo 2:** Agora você deve entrar em cada um dos containers que são referentes a dispositivos. Execute o comando abaixo.
```
$ docker exec -it <ID ou nome do contêiner> bash
```
**Passo 3:** Já no terminal do container do dispositivo, você deve executar o comando abaixo para iniciar o dispositivo.
```
$ python main.py
```
**Passo 4:** Repita os passos 2 e 3 para todos os containers de dispositivos. 

### 0.3 Iniciando a aplicação gráfica
Para executar a aplicação gráfica é preciso navegar até a pasta da mesma e executar o arquivo python principal, para isso execute os comandos abaixo. 
```
$ cd aplicacaoGF/ 
$ python main.py
```

# Explicação da organização do código
Cada pasta possui um dos elementos do sistema a ser desenvolvido, sendo eles: a aplicação gráfica, o middleware e o dispositivo. Na figura abaixo é possível ver como se dá a relação de comunicação entre os mesmos.

![Arquitetura da Solução](img/arquitetura_solucao.png)

A aplicação deve requisitar os dados que precisa ao Broker, por meio de requisições HTTP que foram expostas pela API Restfull desenvolvida no Broker, sendo eles: os dispositivos conectados no broker e os dados dos dispositivos conectados ao broker. A aplicação, ainda, deve enviar comandos ao Broker por meio de requisições HTTP e tais comandos devem ser repassados aos dispositivos especificados.


O dispositivo não deve saber da existência da aplicação, pois o mesmo só se comunica com o Broker. O dispositvo envia os dados de sua leitura por meio do protocolo UDP para o Broker e deverá receber os comandos, provenientes da aplicação gráfica, por meio do protocolo TCP.

Em 'aplicacaoGF' está o código responsável pelo processo da aplicação gráfica que envia comandos para o broker e requisita dados utilizando o padrão HTTP. 

Em 'dispositivo' tem os arquivos necessários a execução do processo do device. Em 'config.py' tem as infoormações para realizar as comunicações com o broker, como as portas TCp e UDP que o mesmo escuta, bem como seu endereço IPv4. Ainda em 'config.py' há a key que será usada para que o dispositivo consiga se conectar e se autenticar com o broker, e tammbém há o segredo que serve como chave para criptografar os dados que serão enviados e descriptografar os recebidos. Em 'interface.py' estão os arquivos referentes as rotinas executadas na thread que trata do menu ao qual o usuário poderá alterar dados e inserir comandos para o dispositivo. Os arquivos 'myTcpSet.py' e 'myUdpSet.py' tratam das rotinas executadas nas threads que lidam com o protocolo TCP e UDP respectivamente. 'Device.py' apresenta a classe que representa o dispositivo.

Em 'middleware' estão os arquivos referentes ao processo do Broker. Em 'config.py' tem as infoormações para realizar as comunicações com o os dispositivos e a aplicação, como as portas TCp e UDP que o mesmo escuta, bem como os endereços IPv4 que a API Restfull irá permitir receber requisições e os endereços ao qual se aceitará conexões TCP. Ainda em 'config.py' há as informações necessárias para autenticação dos dispositivos e criptografia das informações, bem como apresentado em 'dispositivo'. Os arquivos 'SERVER_TCP.py' e 'SERVER_UDP.py' tratam das rotinas executadas nas threads que lidam com o protocolo TCP e UDp respectivamente. 'Broker.py' apresenta a classe que representa o broker e nele há toda a gerência dos dispositivos conectados e seus respectivos tópicos. Em 'api.py' tem a declaração dos endpoints e tudo o mais relacionado a API Restful, porém fez-se do arquivo o main de todo o processo, então tem-se a iniciação dos sockets e etc.

# 1. Introdução
# 2. Fundamentação Teórica
# 3. Metodologia
Todas as comunicações UDP ocorrem pela porta 12346, as TCP são na porta 12345.
O broker só permite que cada tópico de dados tenha apenas um único publicador, e cada tópico de comandos tem apenas um único ouvinte
## 3.1 Aplicação gráfica
## 3.2 Middleware
### 3.2.1 API Restfull
Quais são os verbos e rotas executados na camada de aplicação.

A API Rest possui 5 endpoints, ou rotas.
- O endpoint '/', acessado por uma requisição GET, que é usado para verificar se a aplicação está disponível.

- O endpoint '/pub/TOPIC' (onde TOPIC é um parametro GET que deve conter o nome de um tópico), acessado por uma requisição POST, que é usado publicar um comando, emitido pela aplicação, no tópico especificado. É emitido um status 403 caso a  aplicação tente publicar em um tópico não permitido, 400 se não enviar a estrutura que se espera, 201 caso consiga registrar e 200 caso receba mas não consiga.
- O endpoint '/sub'
- O endpoint '/sub/TOPIC'
- O endpoint '/device_names'




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
    '''Pega uma mensagem de um topico. É utilizado para ler um dado de um dispositivo especifico'''
    # Se não for um tópico permitido, já encerra e retorna o status
    if not topic.startswith('data_'):
        return jsonify({"erro": "Você não tem permissão para este topico"}), 403
    msg = broker.pop_message(topic)
    # Aqui você pode implementar a lógica para ler as mensagens do tópico MQTT
    # Neste exemplo, retornaremos uma lista vazia
    return jsonify({'value': msg}), 200


@app.route('/device_names', methods=['GET'])
@cache.cached(timeout=2) # Cache válido por 2 segundos
def get_devices():
    '''Obtem os nomes dos dispositivos com conexões ativas no Broker
    Return.
        - A lista com o nome de dispositivos conetados ao Broker
            EX: ['Dispositivo_1', 'Dispositivo_2']
    '''
    return jsonify(broker.get_registered_devices()), 200
### 3.2.2 Broker
## 3.3 Device
# 4. Resultados
# 5. Conclusões