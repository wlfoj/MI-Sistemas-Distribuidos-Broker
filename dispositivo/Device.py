from enum import Enum
import time

class Status (Enum):
    Off = 0
    On = 1
    Pause = 2


##  classe dispositivo aqui,
class Sensor:
    dado = 0 # Dado que o sensor está lendo
    status = Status.Off # Se estiver ligado será True

    def __init__(self, nome):
        self.nome = nome

    def ler_dados(self):
        '''Função que retorna o dado da leitura atual do dispositivo.
        Return.
            self.dado (int) -> valor da leitura'''
        return self.dado
    
    def ligar(self):
        self.status = Status.On
    
    def desligar(self):
        self.status = Status.Off

    def pausar(self):
        '''Função que pausa o dispositivo, caso o mesmo esteja ligado'''
        # Só pausa se estiver ligado
        if self.status == Status.On:
            self.status = Status.Pause
    ########?????  E O DESPAUSAR ???????? #######
    def resume(self):
        '''Função que retira o dispositivo do pause, caso ele esteja ligado'''
        if self.status== Status.Pause:
            self.status = Status.On

    def obter_status(self):
        '''Função que informa se o sensor está ligado, desligado ou pausado.
        Return.
            self.status (Status) - > A situação atual do sensor
                Pode ser um dos [ON, OFF, PAUSE]'''
        return self.status
    
    def alterar_dado(self, valor):
        ''' Função para alterar o dado manualmente.
        '''
        # Acho que vou precisar fazer um lock aqui
        while abs(round(self.dado,1) - round(valor,)) > 0.1:  # Defina uma margem de tolerância adequada para o seu caso
            if self.dado < valor:
                self.dado += 0.1  # Ou qualquer incremento que desejar
            else:
                self.dado -= 0.1  # Ou qualquer decremento que desejar
            print("A temp está em", self.dado)
            time.sleep(1)
