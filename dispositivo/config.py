# São endereços IPv4
import os
import base64


# Obtém o valor da variável de ambiente 'NOME' ou retorna 'DISP' se não estiver definida
conf = {
    'key_conn': 'em terra de rei tem ouro', # Para que o broker me aceite
    "broker_host_ip":'192.168.0.2',
    "broker_host_port_udp": 12346,
    "broker_host_port_tcp": 12345,
    "NAME_DEVICE": os.environ.get('NAME_DEVICE', ' '),
    "key_crypt": base64.urlsafe_b64encode(b'Jupiter ser feliz com Netuno   ,') # Para usar no construtor do FERNET
}
