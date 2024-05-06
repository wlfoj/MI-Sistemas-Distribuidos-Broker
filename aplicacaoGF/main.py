import tkinter as tk
from tkinter import ttk, messagebox
import sys

import requests


## =============================== BLOCO DE INICIALIZAÇÃO DE VARIAVEIS =============================== ##
argument = sys.argv # Obtém os argumentos da linha de comando
url_api = "http://"+ argument[1] +":5005"
command_options = ["Ligar", "Desligar", "Pausar", "Continuar"]
devices_list = []
INTERVAL_UPDATE_TIME = 2000 # Apresenta o intervalo de tempo para fazer uma nova requisição para a API

## =============================== BLOCO DE FUNÇÕES PARA INICIALIZAÇÃO =============================== ##
def get_devices():
    '''Função que obtem os dispositivos conectados/permitidos no broker. Deve ser executa ao iniciar a aplicação, e de tempos em tempos.
    Return.
        response (list) -> Lista com os identificadores de cada dispositivo
            ex: response = ['Dispositivo 1', 'Dispositivo 2']
    '''
    response = None
    # URL do endpoint que você deseja acessar
    url = url_api+"/device_names"
    # Realiza a requisição GET
    try:
        response = requests.get(url).json()
        response = response['data']
    except:
        pass

    return response


def send_command():
    '''Função para enviar o comando, via http, para api do broker. Em caso de envio e confirmação do broker, exibe uma mensagem de sucesso
    '''
    ## Obtendo os valores nos inputs
    selected_command = command_input.get()
    selected_device = device_input.get()
    ## Gerando o nome do topico a partir do número do dispositivo
    topic_name = "command_"
    topic_name = topic_name + selected_device.split('_')[1] # Pega o número do dispositivo
    url = url_api+"/pub/"+ topic_name
    # Monta os dados
    dados = {'message': selected_command, 'topico': topic_name, 'remetente': 'aplicação'}
    erro = False
    # faz envio
    try:
        response = requests.post(url, json=dados)
    except:
        erro = True
    # Exibe uma mensagem de erro ou sucesso na tela
    if (response.status_code in [200, 201]) and (not erro):
        messagebox.showinfo("Sucesso", "A solicitação foi enviada com sucesso!")
    else:
        messagebox.showinfo("Erro", "A solicitação não pode ser enviada")
    return 0



## =============================== BLOCO PARA CRIAR A INTERFACE =============================== ##
# Criando a janela principal
root = tk.Tk()
root.title("Aplicação Cliente")

# Frame para a seção de envio de comando
frame_send_command = ttk.LabelFrame(root, text="Enviar Comando")
frame_send_command.pack(padx=10, pady=10, fill="both", expand=True)

# Variáveis para armazenar as opções selecionadas
command_input = tk.StringVar()
device_input = tk.StringVar()

# Dropdown para selecionar o tipo de comando
command_label = ttk.Label(frame_send_command, text="Tipo de Comando:")
command_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
command_type_dropdown = ttk.Combobox(frame_send_command, textvariable=command_input, values=command_options, state='readonly')
command_type_dropdown.grid(row=0, column=1, padx=5, pady=5)

# Dropdown para selecionar o dispositivo
device_label = ttk.Label(frame_send_command, text="Dispositivo:")
device_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
device_dropdown = ttk.Combobox(frame_send_command, textvariable=device_input, values= devices_list, state='readonly')
device_dropdown.grid(row=1, column=1, padx=5, pady=5)

# Botão para enviar o comando
send_button = ttk.Button(frame_send_command, text="Enviar Comando", command=send_command)
send_button.grid(row=2, columnspan=2, padx=5, pady=5)

# Frame para a seção de dados recebidos
frame_table_data_received = ttk.LabelFrame(root, text="Dados Recebidos")
frame_table_data_received.pack(padx=10, pady=10, fill="both", expand=True)

# Tabela para exibir os dados recebidos
table_columns = ("Dispositivo", "Valor Leitura")
table = ttk.Treeview(frame_table_data_received, columns=table_columns, show="headings")
for col in table_columns:
    table.heading(col, text=col)
table.pack(fill="both", expand=True)


## =============================== BLOCO PARA ATUALIZAR VALORES EXIBIDOS =============================== ##
# Função para atualizar a tabela com os dados recebidos
def update_table():
    response = None
    # URL do endpoint que você deseja acessar
    url = url_api+"/sub"
    # Realiza a requisição GET
    erro = False
    try:
        response = requests.get(url).json()
        response = response['data']
    except:
        erro = True
    if response:
        for row in table.get_children():
            table.delete(row)
        for dado in response:
            aux = (dado['device_name'], dado['value'])
            table.insert("", "end", values=aux)


def update_devices_list():
    '''Atualiza a lista de dispositivos na interface gráfica.'''
    global devices_list
    devices_list = get_devices()
    device_dropdown['values'] = devices_list


def update_periodically():
    # Atualiza a tabela de (NOME_DISP, VALOR LIDO)
    update_table()
    # Atualiza a lista de dispositivos
    update_devices_list()
    # faz a atualização a cada x ms
    root.after(INTERVAL_UPDATE_TIME, update_periodically)

# Chamando a função para atualizar periodicamente
update_periodically()




# Rodando a aplicação
root.mainloop()
