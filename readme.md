# Explicação da organização do código
Cada pasta possui um dos elementos do sistema a ser desenvolvido. Em 'aplicacaoGF' eestá o código responsável pelo processo da aplicação gráfica que envia comandos para o broker e requisita dados utilizando o padrão HTTP. 

Em 'dispositivo' tem os arquivos necessários a execução do processo do device. Em 'config.py' tem as infoormações para realizar as comunicações com o broker, como as portas TCp e UDP que o mesmo escuta, bem como seu endereço IPv4. Ainda em 'config.py' há a key que será usada para que o dispositivo consiga se conectar e se autenticar com o broker, e tammbém há o segredo que serve como chave para criptografar os dados que serão enviados e descriptografar os recebidos. Em 'interface.py' estão os arquivos referentes as rotinas executadas na thread que trata do menu ao qual o usuário poderá alterar dados e inserir comandos para o dispositivo. Os aruqivos 'myTcpSet.py' e 'myUdpSet.py' tratam das rotinas executadas nas threads que lidam com o protocolo TCP e UDP respectivamente. 'Device.py' apresenta a classe que representa o dispositivo.

Em 'middleware' estão os arquivos referentes ao processo do Broker. Em 'config.py' tem as infoormações para realizar as comunicações com o os dispositivos e a aplicação, como as portas TCp e UDP que o mesmo escuta, bem como os endereços IPv4 que a API Restfull irá permitir receber requisições e os endereços ao qual se aceitará conexões TCP. Ainda em 'config.py' há as informações necessárias para autenticação dos dispositivos e criptografia das informações, bem como apresentado em 'dispositivo'. Os arquivos 'SERVER_TCP.py' e 'SERVER_UDP.py' tratam das rotinas executadas nas threads que lidam com o protocolo TCP e UDp respectivamente. 'Broker.py' apresenta a classe que representa o broker e nele há toda a gerência dos dispositivos conectados e seus respectivos tópicos. Em 'api.py' tem a declaração dos endpoints e tudo o mais relacionado a API Restful, porém fez-se do arquivo o main de todo o processo, então tem-se a iniciação dos sockets e etc.

Os arquivos Utils.py contém rotinas que auxiliam ao encryptar e desencryptar os dados.
**!!!!!!!!!!!!!!! PRECISA COLOCAR O MUTEX EM BROKER!!!!!!!!!!!!!!!!!!!!!!!!**

# 0. Passo a passo para execução (FEITO)
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
docker exec -it <ID ou nome do contêiner> bash
```
**Passo 3:** Já no terminal do container do dispositivo, você deve executar o comando abaixo para iniciar o dispositivo.
```
python main.py
```
**Passo 4:** Repita os passos 2 e 3 para todos os containers de dispositivos. 

### 0.3 Iniciando a aplicação gráfica
Para executar a aplicação gráfica é preciso navegar até a pasta da mesma e executar o arquivo python principal, para isso execute os comandos abaixo. 
```
$ cd aplicacaoGF/ 
$ python main.py
```







# 1. Introdução
# 2. Fundamentação Teórica
# 3. Metodologia
Através das sessões discutiu-se a forma a de tratar os dados, os serviços a serem implementados, os tipos de protocolos envolvidos em cada comunicação entre os serviços...
Sendo assim, o sistema desenvolvido consiste em um apliicativo gráfico (aplicação), um middleware (broker) e os sensores e atuadores (dispositivos)

Todas as comunicações 

Analisando o problema, constatou-se que a aplicação deveria ter os
seguintes requisitos: cadastro de um ou mais dipositivos no broker

Deve haver um mecanismo, que será o broker, capaz de abstrair detalhes dos dispositivos para a aplicação. Por meio do broker, a aplicação conseguirá obter dados dos dispositivos e enviar comandos para um dispositivo especificado. O broker deve realizar uma conexão TCP com um dispositivo para que o mesmo consiga enviar os pacotes envolvendo comandos emitidos pela aplicação, e deverá receber os pacotes envolvendo os dados de cada dispositivo seguindo o protocolo UDP. A aplicação irá se comunicar com o broker através dos endpoints expostos em uma API Restfull






cadastramento de um novo cliente, edição e exclusão de um
cliente, listagem dos clientes cadastrados, agendamento de uma nova manutenção,
edição e exclusão de manutenções, listagem das manutenções realizadas ou agendadas,

realização de uma manutenção agendada, impressão de manutenções agendadas e
geração de balanços financeiros.
Os arquivos de textos servem para armazenar a base de dados e foram divididos
da seguinte forma: criou-se uma pasta chamada de ‘clientes’ com o arquivo
‘listaClientes.txt’ dentro, esse arquivo é o responsável por guardar os dados dos clientes;
criou-se uma pasta com o nome ‘balanço’, essa pasta guarda os balanços gerados pelo
usuário; criou-se a pasta ‘impressão’, a mesma recebe os arquivos de impressão, quando
criado pelo usuário; A pasta ‘manutenções’ abriga outras duas pastas, a ‘agendada’ e a
‘realizada’. A pasta ‘agendada’ possui o arquivo ‘ManutencoesAgendadas.txt’ que é
onde os dados das manutenções agendadas são guardados. A pasta ‘realizada’ detém o
arquivo ‘ManutencoesRealizadas.txt’ que é o responsável por armazenar os dados das
manutenções que já foram realizadas.
Com a intenção de evitar possíveis erros quanto à abertura de arquivos para
leitura, foi utilizado o modo de leitura ‘a+’ pois o mesmo cria um arquivo em branco,
caso não exista tal arquivo, diferente do modo ‘r’ que gera erro.
Para realizar a ordenação da lista de cliente, por ordem alfabética, e ordenar a
lista de manutenções agendadas, pela menor data, utilizou-se o algoritmo Insert Sort,
baseado no modelo apresentado pela professora Cláudia, na disciplina de Algoritmo I.
Tal modelo foi escolhido levando em conta o desempenho do mesmo, bem como a
simplicidade em se entender a estrutura do código. O procedimento recebe a lista a ser
organizada e o índice da lista que será observado para organizá-la.
Partindo dos requisitos do sistema, dividiram-se todas as funcionalidades em três
temas, sendo eles: procedimentos para clientes, procedimentos para manutenções e
processamento para o balanço. Para facilitar a navegação do usuário pela aplicação,
desenvolveu-se um sistema com três menus, o menu principal, o menu de clientes e o
menu de manutenções.
Para o desenvolvimento do programa, foi utilizado o sistema operacional
Ubuntu, na versão 20.04 LTS, com o Python, na versão 3.8.5. Além disso, houve a
importação de bibliotecas padrão do Python como a ‘datetime’ e a biblioteca ‘os’.
# 4. Resultados
# 5. Conclusões
Os dispositivos poderiam ter sua própria nomeação, em vez do broker atribuir um nome a cada um

A utilização de um banco de dados poderia reduzir as linhas de código e aumentar a eficiência. Bem como, um tratamento de erros, mais elaborado, para todas as entradas e
em situações onde o usuário delete alguma pasta.


O sistema desenvolvido atende bem aos requisitos apontados pelo problema, porém, apesar de tratar alguns erros quanto à entrada de dados para registros, não
oferece segurança em certos casos específicos, como a utilização de nomes de clientes
com acentos.




Tendo em visto que o software é uma versão introdutória a utilização de bancos
de dados e estruturação de dados. Com o intuito de melhoria na eficiência da aplicação,
uma maior atenção as etapas de cadastro é fundamental. Bem como, buscar reduzir a
quantidade de vezes em que as listas são percorridas nos casos onde se deseja realizar
alguma manutenção. Apesar disso, a aplicação oferece uma idéia de administração de
tarefas que podem vir a ser utilizadas em outros contextos, como lista de tarefas, oferta
de serviços.