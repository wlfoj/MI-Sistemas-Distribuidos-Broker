import socket

HOST = '10.0.0.103'     # Endereço IP do Servidor
PORT = 5000            # Porta que o Servidor está
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (HOST, PORT)
# Colocando um eendereço IP e uma porta no Socket
tcp.bind(origem)
# Colocando o Socket em modo passivo
tcp.listen(1)
print('\nServidor TCP iniciado no IP', HOST, 'na porta', PORT)
try:
    while True:
        # Aceitando uma nova conexão
        conexao, cliente = tcp.accept()
        print('\nConexão realizada por:', cliente)
        print(cliente[0], cliente[1])
        while True:
            # Recebendo as mensagens através da conexão
            print("Entrei na parte que faz o recebimento")
            #mensagem = conexao.recv(1024)
            conexao.send(str("oi").encode())
            print("Já passei da parte que faz o recebimento")
            #if not mensagem:
            #    break
            # Exibindo a mensagem recebida
            #print('\nCliente..:', cliente)
            #print('Mensagem.:', mensagem.decode())

except Exception as e:
    print(e)
    print('Finalizando conexão do cliente', cliente)
    # Fechando a conexão com o Socket
    conexao.close()