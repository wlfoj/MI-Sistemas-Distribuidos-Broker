import socket
import threading


class Broker():

    def __init__(self):
        self.mutex = threading.Lock()
        self._LIMIT_DISP_CONNCTED = 10
        self._disp_num = 0 # Representa o número de disposiitivo conectado
        self._devices = [] # A lista de dispositivos {"device_name":"", "ip": '', "tcp_connection": None}
        #########
        self._topics = {
                    #    # Tópicos de comandos, dispositivos registrados como inscritos
                    #    'comandos_1': {'subscribe':self._devices[0]['ip'], 'publisher':'', 'values': None},
                    #    'comandos_2': {'subscribe':self._devices[1]['ip'], 'publisher':'', 'values': None},
                    #    'comandos_3': {'subscribe':self._devices[2]['ip'], 'publisher':'', 'values': None},
                    #    'comandos_4': {'subscribe':self._devices[3]['ip'], 'publisher':'', 'values': None},
                    #    'comandos_5': {'subscribe':self._devices[4]['ip'], 'publisher':'', 'values': None},
                    #    'comandos_6': {'subscribe':self._devices[5]['ip'], 'publisher':'', 'values': None},
                    #    'comandos_7': {'subscribe':self._devices[6]['ip'], 'publisher':'', 'values': None},
                    #    'comandos_8': {'subscribe':self._devices[7]['ip'], 'publisher':'', 'values': None},
                    #    'comandos_9': {'subscribe':self._devices[8]['ip'], 'publisher':'', 'values': None},
                    #    # Tópicos de dados, dispositivos registrados como publicadores
                    #    'dados_1': {'publisher':self._devices[0]['ip'], 'subscribe':'', 'values': 44},
                    #    'dados_2': {'publisher':self._devices[1]['ip'], 'subscribe':'', 'values': None},
                    #    'dados_3': {'publisher':self._devices[2]['ip'], 'subscribe':'', 'values': None},
                    #    'dados_4': {'publisher':self._devices[3]['ip'], 'subscribe':'', 'values': None},
                    #    'dados_5': {'publisher':self._devices[4]['ip'], 'subscribe':'', 'values': None},
                    #    'dados_6': {'publisher':self._devices[5]['ip'], 'subscribe':'', 'values': 32},
                    #    'dados_7': {'publisher':self._devices[6]['ip'], 'subscribe':'', 'values': None},
                    #    'dados_8': {'publisher':self._devices[7]['ip'], 'subscribe':'', 'values': None},
                    #    'dados_9': {'publisher':self._devices[8]['ip'], 'subscribe':'', 'values': None}
                       }
        


    def get_msg_and_device_to_send_command(self) -> list:
        '''Método que percorre os tópicos de comandos, procurando os que tem mensagem para enviar e monta uma lista com as mensagens,
        o ip e a conexão do destinatário.
        Se não tiver nenhum comando para enviar, recebe lista vazia.
        Return.
            [{"conn": None, "ip": None, "msg": None}, ...]
        '''
        resp = []
        st = {"conn": None, "ip": None, "msg": None}
        # Percorro todo os tópicos
        for chave, item in self._topics.items():
            # Se achei algum tópico com mensagem para enviar, adiciono na lista de operação
            if item['values'] is not None and chave.startswith('command'):
                st['msg'] = self.pop_message(chave) # Pego a mensagem
                st["ip"] = item['subscribe'] # Pego o ip de quem vai receber
                st['conn'] = self.get_conn_by_ip(st["ip"]) # Pego a conexão do ip de quem vai receber
                resp.append(st)
        # retorno a mensagem e a conexão do ouvinte
        return resp


    def _get_conn_for_topic(self, TOPIC: str):
        '''Se não tiver nenhum dispositivo, conn deverá ser None'''
        conn = None
        _topics = self._topics[TOPIC]
        # Pego o nome do device pelo tópico
        device = _topics['subscribe']
        # Procura na lista de dispositivos qual a conexão correspondentes
        for dispositivo in self._devices:
            if dispositivo['device_name'] == device:
                conn = dispositivo['conexao_tcp']
                break
        return conn

    def pega_mensagens_todos__topicss_dados(self):
        res = []
        for chave, item in self._topics.items():
            if chave.startswith('dados_'):
                res.append({'dispositivo': self.translate_ip_inn_name(item['publisher']), 'value': self.pop_message(chave)})
        return res



#### ============ BLOCO DE MÉTODOS AUXILIARES ============ ####  
    def get_topic_name_publisher_by_device_name(self, device_name):
        '''Método para obter os nomes dos tópicos em que um ip está cadastrado como publicador.
        Param.
            device_name (str)       -> Nome do dispositivo que se busca o nome do tópico
        Return.
            topic_name (str)        -> O nome do tópico em que o device_name é publiciador
        '''
        topic_name = None
        # Percorre a lista de tópicos
        for topicName, value in self._topics.items():
            # para cada value = {'publisher': device['ip'], 'subscribe': '', 'values': None}
            if value['publisher'] == ip:
                topic_name = topicName
                break # o break é pq estou suponto ter apenas um
        return topic_name
    

    def get_topic_name_subscriber_by_device_name(self, device_name):
        '''Método para obter os nomes dos tópicos em que um ip está cadastrado como ouvinte.
        Param.
            device_name (str)       -> Nome do dispositivo que se busca o nome do tópico
        Return.
            topic_name (str)        -> O nome do tópico em que o device_name é ouvinte
        '''
        topic_name = None
        # Percorre a lista de tópicos
        for topicName, value in self._topics.items():
            # para cada value = {'publisher': device['ip'], 'subscribe': '', 'values': None}
            if value['subscribe'] == ip:
                topic_name = topicName
                break # o break é pq estou suponto ter apenas um
        return topic_name





    def get_topic_name_publisher_by_ip(self, ip):
        '''Método para obter os nomes dos tópicos em que um ip está cadastrado como publicador.
        Param.
            ip (str)         -> IPv4 do dispositivo que se busca o nome do tópico
        Return.
            topic_name (str) -> O nome do tópico em que o IP é publicador
        '''
        topic_name = None
        # Percorre a lista de tópicos
        for topicName, value in self._topics.items():
            # para cada value = {'publisher': device['ip'], 'subscribe': '', 'values': None}
            if value['publisher'] == ip:
                topic_name = topicName
                break # o break é pq estou suponto ter apenas um
        return topic_name
    

    def get_topic_name_subscriber_by_ip(self, ip):
        '''Método para obter os nomes dos tópicos em que um ip está cadastrado como ouvinte.
        Param.
            ip (str)         -> IPv4 do dispositivo que se busca o nome do tópico
        Return.
            topic_name (str) -> O nome do tópico em que o IP é ouvinte
        '''
        topic_name = None
        # Percorre a lista de tópicos
        for topicName, value in self._topics.items():
            # para cada value = {'publisher': device['ip'], 'subscribe': '', 'values': None}
            if value['subscribe'] == ip:
                topic_name = topicName
                break # o break é pq estou suponto ter apenas um
        return topic_name


    def get_conn_by_device_name(self, device_name):
        '''Método para obter a conexão do dispositivo tendo passado o ip do mesmo. Caso não encontre, retorna None
        Param.
            device_name (str)         -> Nome do dispositivo que se busca a conn
        Return.
            conn (socket.socket)      -> A conexão TCP dispositivo correspondente ao IPv4'''
        conn = None
        for device in  self._devices:
            if device['device_name'] == device_name:
                conn = device['tcp_connection']
                break
        return conn
    

    def get_conn_by_ip(self, ip):
        '''Método para obter a conexão do dispositivo tendo passado o ip do mesmo. Caso não encontre, retorna None
        Param.
            ip (str)                  -> IPv4 do dispositivo que se busca a conn
        Return.
            conn (socket.socket)      -> A conexão TCP dispositivo correspondente ao IPv4'''
        conn = None
        for device in  self._devices:
            if device['ip'] == ip:
                conn = device['tcp_connection']
                break
        return conn


    def get_device_name_by_ip(self, ip):
        '''Método para obter o device_name do dispositivo tendo passado o ip do mesmo. Caso não encontre, retorna None
        Param.
            ip (str)        -> IPv4 do dispositivo que se busca o nome
        Return.
            name (str)      -> O nome do dispositivo correspondente ao IPv4'''
        name = None
        for device in  self._devices:
            if device['ip'] == ip:
                name = device['device_name']
                break
        return name

    def get_ip_by_device_name(self, device_name):
        '''Método para obter o ip do dispositivo tendo passado o nome do mesmo. Caso não encontre, retorna None
        Param.
            device_name (str)        -> O nome do dispositivo que se busca o IPv4
        Return.
            ip (str)                 -> O IPv4 do dispositivo'''
        ip = None
        for device in  self._devices:
            if device['device_name'] == device_name:
                ip = device['ip']
                break
        return ip
    

#### ============ BLOCO DE PUSH E POP BÁSICOS DO BROKER ============ ####   
    def get_data_from_all_devices(self):
        ''' Obtem todos os dados de todos os tópicos de dados de todos os dispositivos
        '''
        data = [] # [{'device_name': str, 'value': int}]
        # Passa em todos os tópicos de dados
        for topicName, value in self._topics.items():
            if topicName.startswith("data_"):
                device_name = 'Dispositivo_' + topicName.split('_')[1]
                value = self.pop_message(topicName)   
                data.append({'device_name': device_name, 'value': value})   
        return data          



    def publish_message(self, TOPIC: str, message: str | int, ip: str) -> bool:
        ''' Publica determinada mensagem no tópico correspondente. Retorna True se conseguir fazer e False se n conseguir.
        Olha se o ip tem autorização pra publicar no topico.
        Param.
            TOPIC     (string)          -> Nome do tópico onde a mensagem será publicada
            message   (str | int)       -> Conteúdo da mensagem
            ip (string)                 -> Endereço ip do dispositivo que quer publicar a mensagem
        Return.
            sucess (bool)               -> True se o processo for concluído sem erro 
        '''
        topico = self._topics[TOPIC]
        self.mutex.acquire()
        # Verifico se ip_device tem permissão de publicar no tópico
        if topico['publisher']== '' or topico['publisher'] == ip:
            # escrevo a mensagem
            topico['values'] = message
        self.mutex.release()


    def read_message(self, TOPIC: str, ip: str) -> int | str:
        ''' Obtem determinada mensagem no tópico correspondente. Retorna a mensagem, se houver, ou None, se não houver mensagem.
        Olha se o ip tem autorização pra ler no topico.
        Param.
            TOPIC     (string)          -> Nome do tópico onde a mensagem será publicada
            ip (string)                 -> Endereço ip do dispositivo que quer publicar a mensagem
        Return.
            message (int | str)         -> A mensagem que está no tópico
        '''
        topico = self._topics[TOPIC]
        # Verifico se ip_device tem permissão de ler do tópico
        if topico['publisher'] == '' or topico['publisher'] == ip:
            # Pego a mensagem
            return self.pop_message(TOPIC)
        return None


    def push_message(self, TOPIC: str, value: str | int):
        ''' Faz a publicação de um valor no tópico
        Param.
            TOPIC     (string)          -> Nome do tópico onde a mensagem será registrada
            value     (str|int)         -> Valor que será registrado no tópico
        '''
        # Obtenho o tópico
        topico = self._topics[TOPIC]
        # Faço o registro do valor no tópico
        self.mutex.acquire()
        topico['values'] =  value
        self.mutex.release()


    def pop_message(self, TOPIC: str) -> int | str:
        ''' Obtem determinada mensagem no tópico correspondente.
        Param.
            TOPIC     (string)          -> Nome do tópico onde a mensagem será buscada
        Return.
            message (int | str)         -> A mensagem no tópico ou None, se n tiver
        '''
        # Encontro o tópico
        topico = self._topics[TOPIC]
        self.mutex.acquire()
        # Se não tiver nenhuma mensagem na fila
        if topico['values'] == None:
            self.mutex.release()
            return None
        # Se tiver mensagem na fila
        else:
            # Pega a mensagem
            resp = topico['values']
            # Retiro da fila
            topico['values'] = None
            self.mutex.release()
            return resp

#### ============ BLOCO DE METODOS USADOS PARA REGISTRAR O DISPOSITIVO NO BROKER ============ ####    
    def register_device(self, conexao: socket.socket, ip: str) -> bool:
        '''Função que registra determinado device em uma estrutura com os dados
        Se receber outra  conexão em um ip já cadastrado, eu rejeito a nova conexão.
        (USADO PARA REGISTRAR O DEVICE)
        '''
        # Procuro descobrir se já tem um dispositivo registrado com determinado IP
        is_registered = self._is_ip_device_registered(ip) # D
        # Só faço o registro se não tiver nenhum cadastrado com o mesmo ip, e se a quantidade de disp cadastrados for menor que o máximo permitido
        if (is_registered == False) and (len(self._devices) < self._LIMIT_DISP_CONNCTED):
            device_name = 'Dispositivo_' + str(self._disp_num) # Dispositivo_4
            device = {"device_name": device_name, "ip": ip, "tcp_connection": conexao}
            self._devices.append(device)
            ## Ao registrar, devo criar os tópicos associados ao dispositivo
            self.create_topics_for_new_device(str(self._disp_num), device)
            # Incremento o numero do proximo dispositivo
            self._disp_num = self._disp_num + 1
            return True
        # Se já está registrado, encerro a conexão da nova tentativa
        else:    
            # libero a conexão recebida
            conexao.close()
            return False


    def create_topics_for_new_device(self, num_device: str, device: dict):
        '''Cria o tópico de dados e o tópico de comandos do dispositivo
        (USADO PARA REGISTRAR O DEVICE)
        '''
        # Cria o tópico de dados do dispositivo
        topicNameData = 'data_' + num_device
        self._topics[topicNameData] = {'publisher': device['ip'], 'subscribe': '', 'values': None}
        # Cria o tópico de comandos do dispositivo
        topicNameCommand = 'command_' + num_device
        self._topics[topicNameCommand] = {'publisher': '', 'subscribe':  device['ip'], 'values': None}


    def _is_ip_device_registered(self, ip: str) -> bool:
        ''' Função que informa se o ip já está registrado na estrutura.
        (USADO PARA REGISTRAR O DEVICE)
        '''
        for dispositivo in self._devices:
            if dispositivo["ip"] == ip:
                return True
        return False
    
    def delete_device(self, ip: str):
        '''Metodo para deletar um dispositivo e seus tópicos da estrutura'''
        device_name = self.get_device_name_by_ip(ip)
        device_num = device_name.split('_')[1]
        ## Deleta o dispositivo da lista de devices
        for device in self._devices:
            # Verifica se o dispositivo para excluir está presente na lista
            if device['ip'] == ip:
                # Remove o dispositivo da lista
                self._devices.remove(device)
        ## Deleta os tópicos associados
        # Deleta o tópico de comando
        topic_name = 'command_' + device_num
        del self._topics[topic_name]
        # Deleta o tópico de dados
        topic_name = 'data_' + device_num
        del self._topics[topic_name]

  
#### ============ BLOCO ============ ####    ??????????????????????????
    def get_topic_to_ip(self, ip: str):
        # Aqui eu pego o nome do device
        device = self._obter_dispositivo_por_ip(ip)
        num = device['device_name'].split('_')[1] # Estou pegando o num dele
        topic = 'dados_'+str(num)
        return topic
        # Aqui eu descubro o tópico dele

#### ============ BLOCO DE METODOS PARA TERCEIROS ============ ####    
    def get_registered_devices(self) -> list:
        ''' Obtem a lista de devices registrados na aplicação.
        (Útil para o uso da aplicação gráfica)
        Return.
            list_device_names (list) -> A lista que só contém nomes de devices permitidos
        '''
        list_device_names = []
        devices = self.get_devices()
        for device in devices:
            list_device_names.append(device['device_name'])
        return list_device_names
    

    def get_devices(self) -> list:
        '''Função que retorna a lista de devices para que eu possa iterar sobre ela'''
        return self._devices