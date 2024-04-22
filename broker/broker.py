

class Broker():

    def __init__(self):
        self.dispositivos = [{"device_name":"Dispositivo1", "ip": '', "topicos_publica": [], "topicos_inscreve": []}, 
                {"device_name":"Dispositivo_2", "ip": '', "topicos_publica": [], "topicos_inscreve": []},
                {"device_name":"Dispositivo_3", "ip": '', "topicos_publica": [], "topicos_inscreve": []},
                {"device_name":"Dispositivo_4", "ip": '', "topicos_publica": [], "topicos_inscreve": []},
                {"device_name":"Dispositivo_5", "ip": '', "topicos_publica": [], "topicos_inscreve": []},
                {"device_name":"Dispositivo_6", "ip": '', "topicos_publica": [], "topicos_inscreve": []},
                {"device_name":"Dispositivo_7", "ip": '', "topicos_publica": [], "topicos_inscreve": []},
                {"device_name":"Dispositivo_8", "ip": '', "topicos_publica": [], "topicos_inscreve": []},
                {"device_name":"Dispositivo_9", "ip": '', "topicos_publica": [], "topicos_inscreve": []}
                ]

    def publish_message(self, TOPIC: str, message: dict, ip_device: str = '0.0.0.0') -> bool:
        ''' publica determinada mensagem no tópico correspondente. Retorna True se conseguir fazer e  false se n conseguir.
        Olha se o ip_device tem autorização pra publicar no topico.
        Param.
            TOPIC     (string)          -> Nome do tópico onde a mensagem será publicada
            message   (dicionário/json) -> Conteúdo da mensagem
            ip_device (string)          -> Endereço ip do dispositivo que quer publicar a mensagem
        Return.
            sucess (bool)               -> True se o processo for concluído sem erro 
        '''
        # Verifico se ip_device tem permissão de publicar no tópico
        # Serializo a mensagem??
        # Registro no tópico / insiro na fila
        pass

    def get_message(self, TOPIC: str, ip_device: str = '0.0.0.0') -> dict:
        ''' Obtem determinada mensagem no tópico correspondente. Retorna True se conseguir fazer e false se n conseguir.
        Olha se o ip_device tem autorização pra ler no topico.
        Param.
            TOPIC     (string)          -> Nome do tópico onde a mensagem será buscada
            ip_device (string)          -> Endereço ip do dispositivo que quer publicar a mensagem
        Return.
            message (dict)              -> A mensagem no tópico ou None, se n tiver
        '''
        # Verifico se ip_device tem permissão de ler no tópico
        # deserializo a mensagem??
        # Tira da fila
        pass

    def get_devices_allowed(self) -> list:
        ''' Obtem a lista de devices registrados e permitidos na aplicação.
        Return.
            list_device_names (list) -> A lista que só contém nomes de devices permitidos
        '''
        list_device_names = []
        for dispositivo in self.dispositivos:
            list_device_names.append(dispositivo['device_name'])
        return list_device_names