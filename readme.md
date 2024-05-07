# TEC502-MI-Concorrência-Conectividade-01: Internet das Coisas

### Sumário 
------------
+ [Como executar no LARSID](#como-executar-no-larsid)
+ [Como executar no computador local](#como-executar-no-computador-local)
+ [Introdução](#1-introdução)
+ [Visão geral](#2-visão-geral-da-arquitetura-da-solução)
+ [Discussão sobre produto](#3-discussão-sobre-produto)
+ &nbsp;&nbsp;&nbsp;[Broker](#31-broker)
+ &nbsp;&nbsp;&nbsp;[Dispositivo](#32-dispositivo)
+ &nbsp;&nbsp;&nbsp;[Aplicação](#33-aplicação)
+ &nbsp;&nbsp;&nbsp;[Comunicações](#34-comunicações-e-protocolos-desenvolvidos)
+ &nbsp;&nbsp;&nbsp;[Aspectos Gerais](#35-aspectos-gerais)
+ [Conclusão](#4-conclusões)

# Como executar no LARSID
É necessário que a Aplicação rode em um computador com [Python](https://www.python.org) 3.11, ou mais recente, instalado. É preciso que o computador tenha o Docker instalado, pois o Broker e os Devices serão executados por  meio de containers.

### 1 Faça pull das imagens utilizadas
Abra o terminal e execute os comandos abaixo para baixar as imagens do Broker e do Device no Doocker Hub.
```
$ docker pull wolivej/middleware_b_i:latest
$ docker pull wolivej/device_i:latest
```
### 2 Iniciando o Broker
Para que tudo funcione da melhor forma, é necessário iniciar o serviço do Broker antes dos demais. Sendo assim, execute o seguinte comando em um determinado computador.
```
$ docker run --network=host -it -p 5005:5005 wolivej/middleware_b_i:latest
```
Anote o endereço IP do computador em que o Broker está rodando.
### 3 Iniciando os Devices
Em um novo terminal, execute o comando, logo abaixo, para criar o serviço do dispositivo e substitua 'ip_do_broker' pelo IP anotado no passo anterior. A variável de ambiente UNIT_MEASUREMENT pode representar qualquer unidade de medida, portanto substitua 'unidade_de_medida' pela que quiser. Coloque uma unidade para cada Device instânciado.
```
$ docker run --network=host -it -e BROKER_IP=ip_do_broker -e UNIT_MEASUREMENT=unidade_de_medida wolivej/device_i:latest
```
Com o container já iniciado, é preciso dar o start no processo do Device. Execute o comando abaixo no container iniciado no código acima.
```
$ python main.py
```
Repita o processo para cada dispositivo que você queira criar.
### 3 Iniciando a Aplicação
Por fim, devemos iniciar a aplicação gráfica que irá consumir os dados do Broker. Baixe o arquivo [main.py](https://github.com/wlfoj/concorrencia-conectividade/blob/main/aplicacaoGF/main.py) e execute o comando abaixo, substituindo 'ip_do_broker' pelo IP anotado no tópico **2**.
```
$ python main.py ip_do_broker
```
Como exemplo:
```
$ python main.py 127.0.0.1
```

# Como executar no computador local
### 1 Criação dos containers
Para criar o sistema de maneira isolada no seu computador, execute o comando abaixo no seu terminal, estando na pasta raiz do projeto. O comando irá criar um container para o Broker e 4 containers para os dispositivos.   
```
$ docker-compose up
```
### 2 Iniciando os dispositivos
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

### 3 Iniciando a aplicação gráfica
Para executar a aplicação gráfica é preciso navegar até a pasta da mesma e executar o arquivo python principal, para isso execute os comandos abaixo. 
```
$ cd aplicacaoGF/ 
$ python main.py 127.0.0.1
```


# 1. Introdução
O avanço da tecnologia tem possibilitado a integração de diversos dispositivos por meio da internet, proporcionando facilitações em atividades de diversas naturezas. A gerência de diversos dispositivos que estão distribuídos em nós pela internet se mostra uma complexidade a ser lidada quando se fala em Internet das Coisas (do inglês Internet of Things, IoT). Tais sistemas distribuídos apresentam uma grande quantidade de dispositivos conectados distribuídos em localizações diversas, e para gerenciar de maneira efetiva todas as comunicações entre dispoositivos, comumente se usar serviços de Broker. O serviço de Broker é capaz de fornecer desacoplamento e escalabilidade no seu sistema, pois apresenta isolamento entre os dispositivos, fazendo com que os mesmos não precisem saber detalhes de todos os outros que integram o sistema.

Diante do apresentado, foi proposto a implementação de um sistema distribuído onde há uma aplicação que deve realizar o controle e leitura de dispositivos por meio de um middleware. O sistema deveria ser desenvolvido utilizando sockets para realizar as comunicações TCP e UDP, porém foi permitido utilizar a biblioteca Flask para desenvolver a API Restfull que fornece endpoints para a aplicação, feita com o tkinter. O sistema desenvolvido possui 3 elementos principais: a Aplicação, o sistema que controla e visualiza os dados dos Dispositivos; o Broker, o intermediário que abstraí a comunicação entre a Aplicação e os Dispositivos; o Dispositivo, responsável por simular o comportamento de um sensor e enviar seus dados e receber comandos. A Aplicação, o Broker e os Dispositivos foram implementados em Python, versão 3.11. O relatório é dividido em 3 partes principais, excluindo a introdução e as etapas de como configurar o sistema, sendo elas: a visão geral do problema desenvolvido, as discussões detalhadas sobre a solução apresentada e as conclusões. 

# 2. Visão geral da arquitetura e componentes da solução
Cada pasta possui um dos elementos do sistema a ser desenvolvido, sendo eles: a Aplicação, o Broker e o Dispositivo. Na figura abaixo é possível ver como se dá a relação de comunicação entre os mesmos.

<p align="center">
  <img src="img\arquitetura_solucao.png" alt="arquitetura" width='400px'>
</p>
<p align="center">Diagrama da arquitetura da Solução. Fonte: Autor</p>

A aplicação deve requisitar os dados que precisa ao Broker, por meio de requisições HTTP que foram expostas pela API Restfull desenvolvida no Broker, sendo tais dados: os dispositivos conectados no broker e os valores dos dispositivos conectados ao broker. A aplicação, ainda, deve enviar comandos ao Broker por meio de requisições HTTP e tais comandos devem ser repassados aos dispositivos especificados.

O Dispositivo não deve saber da existência da Aplicação, pois ambos só se comunica com o Broker. O Dispositvo envia os dados de sua leitura por meio do protocolo UDP para o Broker e deverá receber os comandos, provenientes da Aplicação, por meio do protocolo TCP.

Na pasta 'aplicacaoGF' está o código responsável pelo processo da aplicação gráfica que envia comandos para o broker e requisita dados utilizando o protocolo HTTP. 

Na pasta 'dispositivo' tem os arquivos necessários a execução do processo do device. Em 'config.py' tem as infoormações para realizar as comunicações com o broker, como as portas TCp e UDP que o mesmo escuta, bem como seu endereço IPv4. Ainda em 'config.py' há a key que será usada para que o dispositivo consiga se conectar e se autenticar com o broker, e tammbém há o segredo que serve como chave para criptografar os dados que serão enviados e descriptografar os recebidos. Em 'interface.py' estão os arquivos referentes as rotinas executadas na thread que trata do menu ao qual o usuário poderá alterar dados e inserir comandos para o dispositivo. Os arquivos 'myTcpSet.py' e 'myUdpSet.py' tratam das rotinas executadas nas threads que lidam com o protocolo TCP e UDP respectivamente. 'Device.py' apresenta a classe que representa o dispositivo.

Na pasta 'middleware' estão os arquivos referentes ao processo do Broker. Em 'config.py' tem as infoormações para realizar as comunicações com o os dispositivos e a aplicação, como as portas TCp e UDP que o mesmo escuta, bem como os endereços IPv4 que a API Restfull irá permitir receber requisições e os endereços ao qual se aceitará conexões TCP. Ainda em 'config.py' há as informações necessárias para autenticação dos dispositivos e criptografia das informações, bem como apresentado em 'dispositivo'. Os arquivos 'SERVER_TCP.py' e 'SERVER_UDP.py' tratam das rotinas executadas nas threads que lidam com o protocolo TCP e UDp respectivamente. 'Broker.py' apresenta a classe que representa o broker e nele há toda a gerência dos dispositivos conectados e seus respectivos tópicos. Em 'api.py' tem a declaração dos endpoints e tudo o mais relacionado a API Restful, porém fez-se do arquivo o main de todo o processo, então tem-se a iniciação dos sockets e etc.


# 3. Discussão sobre produto
### 3.1 Broker
O Broker atua como um agente intermediário entre a Aplicação e o Dispositivo. Usou-se uma abordagem de Broker com tópicos para este problema, logo tem-se a Aplicação sendo o publisher em todos os tópicos de comandos e sendo subscribe em todos os tópicos de dados. O Dispositivo é publicador no seu próprio tópico de dados e é ouvinte do seu próprio tópico de comandos. Os Dispositivos, ao se conectarem e serem validados pelo Broker, recebem um tópico de comando e de dados exclusivo.

O Broker repassa os comandos recebidos pela aplicação para os dispositivos respectivos por meio do protocolo TCP. Há uma thread no Broker que busca tópicos com comandos ainda não enviados e os envia. Os comandos enviados pelo Broker são mensagens importantes e não podem ser perdidas no envio, portanto utilizou-se o protocolo TCP, pois o mesmo apresenta uma confiança no seu envio que o UDP não possui.

### 3.2 Dispositivo
O Dispositivo é o elemento responsável por enviar dados para o Broker e receber comandos do mesmo. No Dispositivo há 3 threads: a que envia dados via UDP; a que recebe dados via TCP; a que controla a interface manual do mesmo. Assim que seu processo é iniciado, o mesmo procura estabelecer a conexão com o Broker e, caso a conexão caia, tentará restabelecer uma nova.

Há uma interface, em linha de console, para que um usuário possa realizar operações como: ligar, desligar, pausar, alterar temperatura. Tudo isso é feito sem bloquear o funcionamento do mesmo. Devido ao requisito do problema, só é possível alterar os valores do dispositivos na interface manual. 

<p align="center">
  <img src="img\interface dispositivo.png" alt="interface" width='300px'>
</p>
<p align="center">Imagem da interface manual do dispositivo. Fonte: Autor</p>

Em outra thread há um algoritmo que lida com os comandos recebidos pelo Broker (inicialmente enviados pela Aplicação), para que seja possível que a Aplicação controle o dispositivo remotamente. Esta mesma thread detecta quando uma conexão é destruída ou está com problemas e tenta criar um nova.

A terceira thread é a responsável por fazer o envio via UDP do valor lido pelo sensor para o Broker, isso só será feito caso o mesmo esteja ligado e com uma conexão com o Broker. Os dados são enviados continuamente para o Broker, em intervalos de tempo muito curtos, e por isso os mesmos são enviados via UDP, visto que é mais rápido que o envio via TCP e que não há consequências graves caso uma mensagem seja perdida (outra seria recebida em sequência).


### 3.3 Aplicação
A Aplicação é o elemento utilizado para gerenciar os Dispositivos remotamente, seja enviando comandos ou lendo seus valores. Na mesma será possível enviar comando para um dispositivo especifico, bem como visualizar os valores de todos os que  estão com  conexões ativas no Broker.
<p align="center">
  <img src="img\aplicação grafica.png" alt="aplicação" width="300px">
</p>
<p align="center">Tela da Aplicação. Fonte: Autor</p>
### 3.4 Comunicações e protocolos desenvolvidos
As comunicações TCP entre o Broker e Dispositivo se dão pela porta 12346, as comunicações UDP entre o Broker e o Dispositivo se dão pela porta 12345. A API Restful do Broker está exposta na porta 5005.

Usou-se, em todas as mensagens trocadas, o formato json, pois seria mais fácil para os destinatários pocessarem as mensagens recebidas, visto que a mesma estaria em uma estrutura definida e esperada. Aplicou-se criptografia em todas as mensagens para garantir uma maior segurança ao sistema, visto que qualquer dispositivo poderia tentar se conectar ao Broker. O Broker e o dispositivo devem ter o segredo usado para criptografar e descriptografar as mensagens trocadas.

#### 3.4.1 Registro do dispositivo no Broker
Para que possam fazer parte do sistema, os Dispositivos devem estabelecer uma conexão TCP com o Broker e, imediatamente em seguida, enviar o json criptografado abaixo:
```
# Exemplo de Json enviado para o Broker aceitar a conexão
{
    'key': 'CHAVE DE AUTENTICAÇÃO NO BROKER AQUI'
}
```
O Broker irá retornar um json, criptografado, informando se a conexão foi aceita ou não. Conforme exemplo abaixo.
```
# Exemplo de resposta a conexão
{
    'is_acc': True
}
```

#### 3.4.2 Envio dos dados do Dispositivo para o Broker
O Dispositivo, assim que ligado e conectado ao Broker, enviará os seus dados, pelo protocolo UDP, para o Broker de acordo com o formato abaixo.

```
# Exemplo de dado enviado 
{
    "data": '44 mV',
}
```

#### 3.4.3 Envio dos comandos do Broker para o Dispositivo
O Broker busca, ciclicamente, comandos que ainda não foram enviados para os dispositivos e quando os encontra, envia pelo protocolo TCP. Ao encontrar o comando ainda não enviado a um Dispositivo, o Broker irá buscar a conexão do dispositivo que irá receber tal comando e o enviará como no formato abaixo.
```
# Exemplo de comando enviado 
{
    "command": 'Ligar',
}
```
Há outro comando enviado, periodicamente e independente da aplicação, é o comando 'ping'. Tal comando é enviado para verificar se o Dispositivo continua conectado ao Broker.

#### 3.4.4 API Restful
A comunicação entre a Aplicação e o Broker se dá por meio do protocolo HTTP e dos endpoints fornecidos pela API Restfull do Broker. Abaixo tem-se o detalhamento de cada caso de uso da API, bem como seu endpoint associado e a explicação dos parametrôs.

#### 3.4.4.1 Verificação de saúde do Broker
Descrição: Utilizado para verificar se o Broker está operando.
Endpoint: /
Método: GET
#### 3.4.4.2 Publicação de conteúdo
Descrição: Utilizado para que a aplicação publique os comandos aos dispositivos associados. É emitido status: 403, caso a  aplicação tente publicar em um tópico não permitido; 400, se não enviar a estrutura que se espera: 201, caso consiga registrar e 200, caso receba mas não consiga.
Endpoint: /pub/TOPIC
Método: POST
Parâmetros:
    - TOPIC: Parametro GET usado para especificar o nome do tópico onde se irá publicar o comando.
    - message: Comando que será enviado ao Dispositivo. Deverá ser Ligar, Desligar, Pausar ou Continuar.
```
# Exemplo de requisição no rota /pub/comando_1
{
    'message': 'Ligar'
}
```
#### 3.4.4.3 Obtenção de todos os dados no Broker
Descrição: Utilizado para obter todos os dados de dispositivos que já enviaram seus dados.
Endpoint: /sub
Método: GET
**Exemplo de resposta:**
```
# Exemplo de resposta para a requisição em /sub
{
    'data': [{'device_name': 'Dispositivo_1', 'value': '44 F'},
    {'device_name': 'Dispositivo_2', 'value': '100 V'},
    {'device_name': 'Dispositivo_3', 'value': '2 mV'}]
}
```
#### 3.4.4.4 Obtenção de Dispositivos conectados
Descrição: Utilizado para obter a lista com o nome dos dispositivos cadastrados no Broker.
Endpoint: /device_names
Método: GET
**Exemplo de resposta:**
```
# Exemplo de resposta para a requisição em /sub
{
    'data': ['Dispositivo_1'
            'Dispositivo_2',
            'Dispositivo_3']
}
```







### 3.5 Aspectos gerais
Com intuito de produzir um código legível e bem documentado, todo o código se encontra comentado. Atribuiu-se nomes representativos para variáveis, métodos e classes. Fez-se o emprego do Docker, tanto na etapa de desenvolvimento quanto de produção, para isolar o sistema de eventuais problemas que podem ocorrer ao utilizar uma máquina compartilhada. Com relação a Aplicação, por se tratar de uma interface gráfica em python, escolheu-se manter a mesma fora do Docker, devido a complexidade obtida ao expor a mesma no computador local.

O Broker apresenta suporte a conexões simultâneas de vários dispositivos (no código está limitado a 10 conexões, para fins de testes) e por isso se fez necessário o uso de threads. O Broker possui 5 'subprocessos': o da API Restfull; o que recebe mensagens via UDP; o que envia mensagens via TCP; o que recebe e valida as conexões TCP de dispositivos; o que verifica se algum dispositivo foi desconectado.
Como todas as threads fazem uso de uma área de dados sensíveis, que são os dispositivos registrados e os tópicos associados, naturalmente iria ocorrer de alguma thread apagar elementos de uma lista enquanto a outra thread estivesse iterando-a. Para sanar esse problema, utilizou-se um mutex, assim somente uma thread acessará uma região crítica por vez. 

Com intuito de tornar o sistema confiável e robusto, desenvolveu-se soluções para lidarem com situações critícas, como a desconexão de algum nó (Broker ou Dispositivo). Cada dispositivo é capaz de identificar quando o Broker é desconectado, como tammbém é capaz de estabelecer uma nova conexão com Broker.
O Broker possui mecanismos para detectar quando um dispositivo é desconectado, e atuar removendo o mesmo de sua lista de conexões. Para este trabalho, tanto o Broker quanto o Dispositivo são considerados desconectados quando a conexão TCP apresenta alguma inconsistência.

# 4. Conclusão
O produto desenvolvido atende aos requisitos apresentados na situação problema. Durante o processo de desenvolvimento, pode-se aprender sobre técnicas de redes e aplicadas em sistemas distribuídos (como a conectividade), e também características de sistemas com threads (como a concorrência). Desta forma, este projeto serviu para aprofundar os conhecimentos da disciplina teórica (IPv4, TCP e UDP), como também serviu para a formação profissional.


Embora o sistema implementado atenda de forma eficaz o problema proposto, o mesmo pode ser melhorado em aspectos de algoritmos e na utilização de mais threads para o processamento de requisições. Outro ponto a ser melhorado é a nomeação dos dispositivos, na solução apresentada um determinado dispositivo muda de nome sempre que estabelece nova conexão, poderia haver uma forma de reconhecer que é o mesmo dispositivo de uma conexão anterior para que se fosse atribuído o mesmo nome.