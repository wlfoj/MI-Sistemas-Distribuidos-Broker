import os

from Device import Sensor


def limpar_tela():
    if os.name == 'posix': # Verifica se é um sistema tipo Unix (Linux, macOS, etc.)
        os.system('clear') # Comando para limpar a tela no Unix
    elif os.name == 'nt': # Verifica se é Windows
        os.system('cls') # Comando para limpar a tela no Windows


def decisor(response: int, dispositivo: Sensor):
    match response:
        case 1:
            dispositivo.ligar()
        case 2:
            dispositivo.desligar()
        case 3:
            dispositivo.pausar()
        case 4:
            MenuAlterarDado(dispositivo)


def MenuAlterarDado(dispositivo: Sensor):
    ''' Fluxo para alterar o dado do sensor manualmente
    '''
    while 1:
        try:
            response = int(input("Digite o valor do dado ajustado: "))
            # Aqui eu faço a  validação do valor digitado
            # if response :
            #     raise Exception
            # A temperatura deverá ser incrementada aos poucos
            dispositivo.alterar_dado(response)
        except ValueError as e: 
            print("Você não digitou um número, tente novamente")
            input("Pressione Enter para prosseguir")
        except Exception as e:
            print("Tentre novamente, digite um número válido")
            input("Pressione Enter para prosseguir")   
        limpar_tela()
    
  

# O código deve permitir alterar manualmente a temperatura do sensor
def MenuPrincipal(dispositivo: Sensor):
    ''' Menu principal do sistema, permite que escolha algumas ações. Será uma thread
    '''
    while 1:
        try:
            print("OPÇÕES\n[1]- Para ligar o dispositivo\n[2]- Para desligar o dispositivo\n[3]- Para pausar o dispositivo\n[4]- Para alterar o dado do dispositivo")
            response = int(input("Sua opção: "))
            # faço a validação das opções
            if response not in [1,2,3,4,5]:
                raise Exception
            else:
                decisor(response, dispositivo)
        except ValueError as e: 
            print("Você não digitou um número, tente novamente")
            input("Pressione Enter para prosseguir")
        except Exception as e:
            print("Tentre novamente, digite um número entre 1 e 5")
            input("Pressione Enter para prosseguir")   
        limpar_tela()
