import tkinter as tk
from tkinter import ttk, messagebox

import requests

## =============================== BLOCO DE INICIALIZAÇÃO DE VARIAVEIS =============================== ##
url_api = "http://127.0.0.1:5000"
opcoes_comando = ["Ligar", "Desligar", "Pausar", "Continuar"]
lista_dispositivos = []
## =============================== BLOCO DE FUNÇÕES PARA INICIALIZAÇÃO =============================== ##
def get_devices():#ok
    '''Função que obtem os dispositivos conectados/permitidos no broker. Deve ser executa ao iniciar a aplicação, ou de tempos em tempos.
    Return.
        response (list) -> Lista com os identificadores de cada dispositivo
            ex: response = ['Dispositivo 1', 'Dispositivo 2']
    '''
    response = None
    # URL do endpoint que você deseja acessar
    url = url_api+"/device_names"
    # Realiza a requisição GET
    erro = False
    try:
        response = requests.get(url).json()
    except:
        erro = True

    if (not erro):
        messagebox.showinfo("Sucesso", "A solicitação foi enviada com sucesso!")
    else:
        messagebox.showinfo("Erro", "A solicitação não pode ser enviada")
    return response


def enviar_comando():#ok
    '''Função para enviar o comando, via http, para api do broker. Em caso de envio e confirmação do broker, exibe uma mensagem de sucesso
    '''
    ## Obtendo os valores nos inputs
    comando_selecionado = tipo_comando_var.get()
    dispositivo_selecionado = dispositivo_var.get()
    ###
    if (comando_selecionado not in opcoes_comando) and (dispositivo_selecionado not in lista_dispositivos):
        messagebox.showinfo("Erro", "Selecione o comando e o dispositivo presente nas opções")
        return 0
    ## Gerando o nome do topico a partir do número do dispositivo
    topic_name = "comando_"
    topic_name = topic_name + dispositivo_selecionado.split('_')[1] # Pega o número do dispositivo
    url = url_api+"/pub"
    # Aqui você pode adicionar lógica para enviar o comando para o dispositivo selecionado
    # Monta os dados
    dados = {'message': comando_selecionado, 'topico': topic_name,'remetente': 'aplicação'}
    erro = False
    try:
        response = requests.post(url, json=dados)
    except:
        erro = True

    if (response.status_code in [200, 201]) and (not erro):
        messagebox.showinfo("Sucesso", "A solicitação foi enviada com sucesso!")
    else:
        messagebox.showinfo("Erro", "A solicitação não pode ser enviada")
    return 0



# Simulação de dados recebidos via TCP
dados_recebidos = [
    ("Dado 1", "Valor 1"),
    ("Dado 2", "Valor 2"),
    ("Dado 3", "Valor 3")
]

lista_dispositivos = get_devices()


## =============================== BLOCO PARA CRIAR A INTERFACE =============================== ##
# Criando a janela principal
root = tk.Tk()
root.title("Aplicação Cliente")

# Frame para a seção de envio de comando
frame_envio_comando = ttk.LabelFrame(root, text="Enviar Comando")
frame_envio_comando.pack(padx=10, pady=10, fill="both", expand=True)

# Variáveis para armazenar as opções selecionadas
tipo_comando_var = tk.StringVar()
dispositivo_var = tk.StringVar()

# Dropdown para selecionar o tipo de comando
tipo_comando_label = ttk.Label(frame_envio_comando, text="Tipo de Comando:")
tipo_comando_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
tipo_comando_dropdown = ttk.Combobox(frame_envio_comando, textvariable=tipo_comando_var, values=opcoes_comando)
tipo_comando_dropdown.grid(row=0, column=1, padx=5, pady=5)

# Dropdown para selecionar o dispositivo
dispositivo_label = ttk.Label(frame_envio_comando, text="Dispositivo:")
dispositivo_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
dispositivo_dropdown = ttk.Combobox(frame_envio_comando, textvariable=dispositivo_var, values= lista_dispositivos)
dispositivo_dropdown.grid(row=1, column=1, padx=5, pady=5)

# Botão para enviar o comando
enviar_botao = ttk.Button(frame_envio_comando, text="Enviar Comando", command=enviar_comando)
enviar_botao.grid(row=2, columnspan=2, padx=5, pady=5)

# Frame para a seção de dados recebidos
frame_dados_recebidos = ttk.LabelFrame(root, text="Dados Recebidos")
frame_dados_recebidos.pack(padx=10, pady=10, fill="both", expand=True)

# Tabela para exibir os dados recebidos
colunas = ("Dado", "Valor")
tabela = ttk.Treeview(frame_dados_recebidos, columns=colunas, show="headings")
for col in colunas:
    tabela.heading(col, text=col)
tabela.pack(fill="both", expand=True)

# Função para atualizar a tabela com os dados recebidos
def atualizar_tabela(dados_recebidos):
    print("Executei o loop")
    response = None
    # URL do endpoint que você deseja acessar
    url = url_api+"/sub"
    # Realiza a requisição GET
    erro = False
    try:
        response = requests.get(url).json()
    except:
        erro = True
    for row in tabela.get_children():
        tabela.delete(row)
    for dado in response:
        aux = (dado['dispositivo'], dado['value'])
        tabela.insert("", "end", values=aux)




def atualizar_periodicamente():
    # Simulando a atualização periódica dos dados recebidos (você pode substituir isso por uma conexão TCP real)
    atualizar_tabela(dados_recebidos + [("Novo Dado", "Novo Valor")])
    root.after(5000, atualizar_periodicamente)

# Chamando a função para atualizar periodicamente
atualizar_periodicamente()

# Rodando a aplicação
root.mainloop()
