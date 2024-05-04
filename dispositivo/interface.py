import os

from Device import Sensor, Status

# import logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def cleanScreen():
    if os.name == 'posix': # Verifica se é um sistema tipo Unix (Linux, macOS, etc.)
        os.system('clear') # Comando para limpar a tela no Unix
    elif os.name == 'nt': # Verifica se é Windows
        os.system('cls') # Comando para limpar a tela no Windows


def decisionMaker(response: int, device: Sensor):
    match response:
        case 1:
            device.set_status(Status.On)
        case 2:
            device.set_status(Status.Off)
        case 3:
            device.set_status(Status.Pause)
        case 4:
            changeDataMenu(device)


def changeDataMenu(device: Sensor):
    ''' Fluxo para alterar o dado do sensor manualmente
    '''
    while 1:
        try:
            response = int(input("Digite o valor do dado ajustado: "))
            # Aqui eu faço a  validação do valor digitado
            # if response :
            #     raise Exception
            # A temperatura deverá ser incrementada aos poucos
            device.change_data(response)
        except ValueError as e: 
            print("Você não digitou um número, tente novamente")
            input("Pressione Enter para prosseguir")
        except Exception as e:
            print("Tentre novamente, digite um número válido")
            input("Pressione Enter para prosseguir")   
        cleanScreen()
    
  

def mainMenu(device: Sensor):
    ''' Menu principal do sistema, permite que escolha algumas ações. Será uma thread    '''
    # logging.info(f'MENU - Thread para controle de dispositivo manualmente iniciada')
    while 1:
        try:
            print(f"O dispositivo está {device.get_status()} com dado de leitura {device.get_data()}")
            print("OPÇÕES\n[1]- Para ligar/despausar o dispositivo\n[2]- Para desligar o dispositivo\n[3]- Para pausar o dispositivo\n[4]- Para alterar o dado do dispositivo")
            response = int(input("Sua opção: "))
            # faço a validação das opções
            if response in [1,2,3,4] :
                decisionMaker(response, device)
            else:
                raise Exception
                # Se a resposta estiver dentro das possibilidades esperadas, tomo a ação determinada
                
        except ValueError as e: 
            print("Você não digitou um número, tente novamente")
            input("Pressione Enter para prosseguir")
        except Exception as e:
            print("Tentre novamente, digite um número entre 1 e 5")
            input("Pressione Enter para prosseguir")   
        cleanScreen()
