Não será permitido criar novos tópicos que já n estejam iniciados

Ao receber uma requisição eu vou precisar validar a requisição body e params e etc

vou permitir que determinado dispositivo se conecte e diga em qual tópico ele vai assinar e em qual ele  vai publicar. Preciso validar ele para permitir que ele consiga se cadastrar

Usar logs para saber quando o cara está se conectando e para saber qual o tópico que ele conecta e de onde ele está lendo tambpém e publica

O broker só vai permitir os acessos especificos. exemplo, o cliente só vai poder publicar nas filas de comando e só vai poder ouvir das filas de dados. a logica dos dispositivos é o contrario, porém ele só pode ouvir da sua propria fila de comando, e só publica na sua propria fila de dados

vai ter um endpoint que pega dados de um fila especifica
vai ter um endpoint que publica dados de uma fila especifica
vai ter um endpoint que pega os dados de todas as filas de comandos
vai ter um endpoint que pega os dados de todas as filas de dados
vai ter um endpoint que pega os dados de todas as filas de comandos + dados
Vai ter um endpoint que obtem a lista de todos os dispositivos do broker

Vai ter um parser para controlar o formato que vai receber dos dados