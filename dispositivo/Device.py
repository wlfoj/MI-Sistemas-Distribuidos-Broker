from enum import Enum
import time
import random

class Status (Enum):
    Off = "Desligado"
    On = "Ligado"
    Pause = "Pausado"


##  classe dispositivo aqui,
class Sensor:
    _data = 0 # Dado que o sensor está lendo
    _status = Status.Off # Se estiver ligado será True

    def __init__(self, nome, dado_inicial, unidade):
        self._nome = nome
        self._data = dado_inicial
        self._unit_measurement = unidade

    def get_unit_measurement(self):
        return self._unit_measurement
    
    def get_data(self):
        '''Função que retorna o dado da leitura atual do dispositivo. A cada leitura o dado é atualizado aleatóriamente em torno do ponto anterior.
        Return.
            self.dado (int) -> valor da leitura'''
        # Atualizando o valor
        f = random.randint(-100, 100)/100
        self._data = self._data + f
        # 
        return round(self._data, 2)
    
    def set_status(self, new_status: Status):
        # Se tentei pausar, mas a aplicação não estava ligada
        if self._status != Status.On and new_status == Status.Pause:
            pass
        else:
            self._status = new_status


    def get_status(self):
        '''Função que informa se o sensor está ligado, desligado ou pausado.
        Return.
            self._status (Status) - > A situação atual do sensor
                Pode ser um dos [ON, OFF, PAUSE]'''
        return self._status
    
    def change_data(self, valor):
        ''' Função para alterar o dado manualmente.        '''
        # Só altera se a aplicação estiver ligada
        if self._status == Status.On:
            self._data = valor
