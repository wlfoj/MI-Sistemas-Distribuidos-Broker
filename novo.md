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
Por fim, devemos iniciar a aplicação gráfica que irá consumir os dados do Broker. Execute o comando abaixo, substituindo 'ip_do_broker' pelo IP anotado no passo **0.2**.
```
$ python main.py ip_do_broker
```
Como exemplo:
```
$ python main.py 127.0.0.1
```



# Como a arquitetura foi desenvolvida. Quais os componentes e como eles se comunicam. Qual a ordem das mensagens trocadas.
A arquitetura da solução desenvolvida apresenta 3 componentes principais: o middleware, ou Broker; o dispositivo; a aplicação.


## Comunicação entre Dispositivo e Broker
Quando um dispositivo deseja se conectar com o Broker, o mesmo precisa realizar uma conexão TCP com o Broker. Após realizar a conexão, o dispositivo deve enviar uma mensagem, json, criptrografada contendo uma chave que será usada no Broker para decidir se o dispositivo poderá ser cadastrado ou não no middleware. Caso a chave enviada pelo dispositivo esteja em conformidade com a esperada pelo Broker, o dispositivo será registrado e terá tópicos associados ao mesmo, e após a validação pelo broker, será enviado um json ao dispositivo informando se a chave foi aceita ou não. O dispositivo se encerrará caso a chave de autenticação não seja aceita, visto que não é nenhum problema no sistema distribuído e sim no código fonte do dispositivo que está com a chave incorreta. 


# Protocolos usados entre o Device e o Broker
Caso a conexão seja feita, o mesmo irá enviar continuamente os dados de suas leituras com o protocolo UDP, isto é, caso o mesmo esteja ligado. Os dados são enviados continuamente para o Broker, em intervalos de tempo muito curtos, e por isso os mesmos são enviados via UDP, visto que é mais rápido que o envio via TCP e que não há consequências graves caso uma mensagem seja perdida (outra seria recebida em sequência).

O Broker repassa os comandos recebidos pela aplicação para os dispositivos respectivos por meio do protocolo TCP. Há uma thread no Broker que busca tópicos com comandos ainda não enviados e os envia. Os comandos enviados pelo Broker são mensagens importantes e não podem ser perdidas no envio, portanto utilizou-se o protocolo TCP, pois o mesmo apresenta uma confiança no seu envio que o UDP não possui.


# Como threads foram usados para tornar o sistema mais eficiente? Há problemas de concorrência decorrentes do uso de threads? Se sim, como estas questões foram tratadas?
O Broker apresenta suporte a conexões simultâneas de vários dispositivos (o produto está limitado a 10 conexões, para fins de testes) e por isso se fez necessário o uso de threads. O Broker possui 5 'subprocessos': o da API Restfull; o que recebe mensagens via UDP; o que envia mensagens via TCP; o que recebe e válida as conexões de dispositivos; o que verifica se algum dispositivo foi desconectado.
Como todas as threads fazem uso de uma área de dados sensíveis, que são os dispositivos registrados e os tópicos associados, naturalmente, iria ocorrer de alguma thread apagar elementos de uma lista enquanto a outra thread estivesse iterando-a. Para sanar esse problema, fez-se necessário utilizar um mutex, assim somente um thread acessará uma região crítica por vez. 

No dispositivo há 3 threads: a que ennvia dados via UDP; a que recebe dados via TCP; a que controla a interface manual do mesmo.