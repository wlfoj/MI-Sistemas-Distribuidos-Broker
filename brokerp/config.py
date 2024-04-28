import base64

conf = {
    'key_conn': 'em terra de rei tem ouro', # Como permito conexão de qualquer IP, devo verificar isso
    'tcp_addres_con': "0.0.0.0", # Qualquer IPv4
    'tcp_port': 12345,
    "udp_port": 12346,
    "key_decrypt": base64.urlsafe_b64encode(b'Jupiter ser feliz com Netuno   ,') # Para usar no construtor do FERNET
}