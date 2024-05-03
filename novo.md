# TEC502-MI-Concorrencia-01
 
## Como executar a solução:

É necessário ter o [Python](https://www.python.org), versão 3.11 ou mais recente, instalado na sua máquina para rodar a aplicação gráfica.Como também precisa-se do Docker instalado, pois o mesmo será usado para instânciar e isolar 2 elementos do produto desenvolvido ( o middleware e o device).

### Obtendo as imagens:
Baixe as imagens do DockerHub para sua máquina com os comandos abaixo:
```
$ docker pull wolivej/middleware_b_i
$ docker pull wolivej/device_i
```

### Executandos as imagens obtidas:
Agora é preciso executar as imagens obtidas no passo anterior. Comece iniciando o middleware/broker.
Após a obtenção das imagens será necessário executá-las. A primeira imagem a ser executada deve ser o broker, porque ela fornece o IP que será passado para a imagem seguinte:
```
docker run -it -p 5025:5025 vanderleicio/dispositivo
```
Copie o número do IP do Broker e passe como variável de execução da imagem dos Dispositivos (no lugar de {broker_ip}):
```
docker run -it -e broker_ip={broker_ip} vanderleicio/dispositivo
```

### Executando a aplicação:
Baixe o arquivo [aplicacao.py]([https://gist.github.com/usuario/linkParaInfoSobreContribuicoes](https://github.com/Vanderleicio/TEC502-MI-Concorrencia-01/blob/main/aplicacao/aplicacao.py)) e o execute com o comando:
```
python aplicacao/aplicacao.py
```
Pronto, a solução já está executando e funcionando.