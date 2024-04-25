falta ver se a aplicação grafica só exibi os dados do sensor selecionado ou de todos
falta testar a parte do tcp e udp no dispositivo
falta colocar o mutex na parte que usa o dado, para que n ocorra de enviar um dado incoerente no dispositivo







Se na hora de enviar os dados via tcp do broker pro dispositivo, houver um erro. Vou considerar que o dispositivo foi desplugado e então removo ele da minha lista de conexões




Fazer o dispositivo receber um comando do broker
Fazer o broker receber um dado do sensor
Fazer a aplicação enviar comando pro broker que envia para o sensor
Fazer o sensor enviar um comando para o broker que vai aguardar a requisição da api 

Fazer a parte da conexão dinamica. Quando o dispositivo conecta eu registro a conexão na estrututra de dados 

Fazer a parte do docker para atribuir um ipv4 ao sensor correto. Instânciar até 5 sensores