import socket
from typing import Tuple
from config import conf

from enum import Enum

class Modes(Enum):
    DIRECT = 1
    FAN_OUT = 2
    FAN_IN = 3
    NO_QUEUE = 4

class Broker():

    def __init__(self, mode: Modes):
        self._mode = mode
        self._dispositivos = [
                {"device_name":"Dispositivo_1", "ip": '', "conexao_tcp": None}, 
                {"device_name":"Dispositivo_2", "ip": '', "conexao_tcp": None},
                {"device_name":"Dispositivo_3", "ip": '', "conexao_tcp": None},
                {"device_name":"Dispositivo_4", "ip": '', "conexao_tcp": None},
                {"device_name":"Dispositivo_5", "ip": '', "conexao_tcp": None},
                {"device_name":"Dispositivo_6", "ip": '', "conexao_tcp": None},
                {"device_name":"Dispositivo_7", "ip": '', "conexao_tcp": None},
                {"device_name":"Dispositivo_8", "ip": '', "conexao_tcp": None},
                {"device_name":"Dispositivo_9", "ip": '', "conexao_tcp": None}
                ]
        #########
        self.topico = {
                       # Tópicos de comandos, dispositivos registrados como inscritos
                       'comandos_1': {'subscribe':self._dispositivos[0]['device_name'], 'publisher':'', 'values': None},
                       'comandos_2': {'subscribe':self._dispositivos[1]['device_name'], 'publisher':'', 'values': None},
                       'comandos_3': {'subscribe':self._dispositivos[2]['device_name'], 'publisher':'', 'values': None},
                       'comandos_4': {'subscribe':self._dispositivos[3]['device_name'], 'publisher':'', 'values': None},
                       'comandos_5': {'subscribe':self._dispositivos[4]['device_name'], 'publisher':'', 'values': None},
                       'comandos_6': {'subscribe':self._dispositivos[5]['device_name'], 'publisher':'', 'values': None},
                       'comandos_7': {'subscribe':self._dispositivos[6]['device_name'], 'publisher':'', 'values': None},
                       'comandos_8': {'subscribe':self._dispositivos[7]['device_name'], 'publisher':'', 'values': None},
                       'comandos_9': {'subscribe':self._dispositivos[8]['device_name'], 'publisher':'', 'values': None},
                       # Tópicos de dados, dispositivos registrados como publicadores
                       'dados_1': {'publisher':self._dispositivos[0]['device_name'], 'subscribe':'', 'values': 44},
                       'dados_2': {'publisher':self._dispositivos[1]['device_name'], 'subscribe':'', 'values': None},
                       'dados_3': {'publisher':self._dispositivos[2]['device_name'], 'subscribe':'', 'values': None},
                       'dados_4': {'publisher':self._dispositivos[3]['device_name'], 'subscribe':'', 'values': None},
                       'dados_5': {'publisher':self._dispositivos[4]['device_name'], 'subscribe':'', 'values': None},
                       'dados_6': {'publisher':self._dispositivos[5]['device_name'], 'subscribe':'', 'values': 32},
                       'dados_7': {'publisher':self._dispositivos[6]['device_name'], 'subscribe':'', 'values': None},
                       'dados_8': {'publisher':self._dispositivos[7]['device_name'], 'subscribe':'', 'values': None},
                       'dados_9': {'publisher':self._dispositivos[8]['device_name'], 'subscribe':'', 'values': None}
                       }
        


    def publish_message(self, TOPIC: str, message: dict, ip: str) -> bool:
        ''' publica determinada mensagem no tópico correspondente. Retorna True se conseguir fazer e  false se n conseguir.
        Olha se o ip_device tem autorização pra publicar no topico.
        Param.
            TOPIC     (string)          -> Nome do tópico onde a mensagem será publicada
            message   (dicionário/json) -> Conteúdo da mensagem
            ip_device (string)          -> Endereço ip do dispositivo que quer publicar a mensagem
        Return.
            sucess (bool)               -> True se o processo for concluído sem erro 
        '''
        topico = self.topico[TOPIC]
        # Verifico se ip_device tem permissão de publicar no tópico
        if topico['publisher']== '' or topico['publisher'] == ip:
            # escrevo a mensagem
            topico['values'] = message


    def pega_mensagem_e_ouvinte(self) -> Tuple[str, socket.socket]:
        msg = None
        conn = None
        # Percorro todo os tópicos
        for chave, item in self.topico.items():
            # Se achei algum tópico com mensagem para enviar
            if item['values'] is not None:
                msg = self.pop_message(chave)
                conn = self._get_conn_for_topic(chave)
                break
        # retorno a mensagem e a conexão do ouvinte
        return msg, conn


    def _get_conn_for_topic(self, TOPIC: str):
        '''Se não tiver nenhum dispositivo, conn deverá ser None'''
        conn = None
        topico = self.topico[TOPIC]
        # Pego o nome do device pelo tópico
        device = topico['subscribe']
        # Procura na lista de dispositivos qual a conexão correspondentes
        for dispositivo in self._dispositivos:
            if dispositivo['device_name'] == device:
                conn = dispositivo['conexao_tcp']
                break
        return conn

    def pega_mensagens_todos_topicos_dados(self):
        res = []
        for chave, item in self.topico.items():
            if chave.startswith('dados_'):
                res.append({'topic':chave, 'value': self.pop_message(chave)})
        return res

    def pop_message(self, TOPIC: str) -> dict:
        ''' Obtem determinada mensagem no tópico correspondente. Retorna True se conseguir fazer e false se n conseguir.
        Olha se o ip_device tem autorização pra ler no topico.
        Param.
            TOPIC     (string)          -> Nome do tópico onde a mensagem será buscada
            ip_device (string)          -> Endereço ip do dispositivo que quer publicar a mensagem
        Return.
            message (dict)              -> A mensagem no tópico ou None, se n tiver
        '''
        # Encontro o tópico
        topico = self.topico[TOPIC]
        # Se não tiver nenhuma mensagem na fila
        if topico['values'] == None:
            return None
        # Se tiver mensagem na fila
        else:
            # Pega a mensagem
            resp = topico['values']
            # Retiro da fila
            topico['values'] = None
            return resp


    def get_registered_devices(self) -> list:
        ''' Obtem a lista de devices registrados e permitidos na aplicação.
        Return.
            list_device_names (list) -> A lista que só contém nomes de devices permitidos
        '''
        list_device_names = []
        for dispositivo in self._dispositivos:
            list_device_names.append(dispositivo['device_name'])
        return list_device_names
    
    ## NECESSÁRIO INCLUIR O MUTEX
    def register_device(self, conexao: socket.socket, ip: str) -> bool:
        '''Função que registra determinado device em uma estrutura com os dados'''
        # Procuro por um slot com o ip especificado na lista de permitidos
        ## Aqui é como se fosse validar, se eu não especificasse os ips, os dispositivos deveriam ter uma key
        dispositivo_slot = self.obter_dispositivo_por_ip(ip)
        # Se eu tiver encontrado algum
        if dispositivo_slot:
            # Faço o registro da conexão
            dispositivo_slot['conexao_tcp'] = conexao
            return True
        else:    
            # libero a conexão recebida
            conexao.close()
            return False

    def _obter_dispositivo_por_ip(self, ip: str):
        for dispositivo in self.dispositivos:
            if dispositivo["ip"] == ip:
                return dispositivo
        return None
    
  
    
    ## NECESSÁRIO INCLUIR O MUTEX
    def register_deviceV2(self, conexao: socket.socket, key: str):
        '''Função que registra determinado device em uma estrutura com os dados'''
        chave_descriptografada = self.cipher.decrypt(key)
        # Se a chave recebida for a mesma permitida
        if chave_descriptografada == conf['key_allowed']:
            # Procuro por um slot livre para registro
            dispositivo_slot = self.obter_slot_livre()
            # Se tiver achado o slot
            if dispositivo_slot:
                # Faço o registro da conexão
                dispositivo_slot['conexao_tcp'] = conexao
                return True
        else:    
            # libero a conexão recebida
            conexao.close()
            return False            
    
    def _obter_slot_livre(self):
        for dispositivo in self._dispositivos:
            # Se tiver um slot sem a conexão preenchida
            if dispositivo["conexao_tcp"] == None:
                return dispositivo
        return None     
    