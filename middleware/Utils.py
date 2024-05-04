from cryptography.fernet import Fernet
import json
from config import conf

class Utils():
    fernet = Fernet(conf['key_decrypt']) 

    @staticmethod
    def encrypt(msg: dict):
        '''Método para encriptar um determinado envio (json/dict)
        Return.
            dado_criptografado -> bytes criptografados'''
        # Serializa o dicionário para JSON STRING(até dumps) em bytes (encode)
        json_string = json.dumps(msg)
        msg_bytes = json_string.encode('utf-8')
        # Criptografa o envio
        dado_criptografado = Utils.fernet.encrypt(msg_bytes)
        return dado_criptografado
    

    @staticmethod
    def decrypt(msg: bytes):
        '''Método para desincriptar um determinado recebimento (bytes)
        Return.
            mensagem_json_dict -> Objeto json/dict'''
        msg = msg.decode('utf-8') 
        # Tira da criptografia
        mensagem_descriptografado = Utils.fernet.decrypt(msg) # Retorna os bytes
        # Converte a mensagem de bytes para string
        mensagem_string = mensagem_descriptografado.decode('utf-8')
        # Transforma a string em json
        mensagem_json_dict = json.loads(mensagem_string)
        return mensagem_json_dict