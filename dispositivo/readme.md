Usar mutex para alterar os dado do dispositivo sem que uma thread de envio esteja enviando um dado desatualizado
- [ ] adicionar um logger
- [ ] Adicionar um lock na variavel de dados?
- VER OQ FAZER QUANDO DÁ ERRO

# Na conexão e registro no broker
Para se registrar na aplicação, o device envia
```
{
    'key': SECRET_HERE
}
```
# Na conexão e registro no broker
Após o envio do device o broker responde
```
{
    'is_acc': True | False
}
```


# Quando quiser mandar um comando para o dispositivo
Recebe no TCP a seguinte a estrutura
```
{
    'command': 'NOME_DO_COMANDO'
}
```


# O dispositivo envia via udp
Envia no UDP a seguinte estrutura
```
{
    'data': VALOR_DA_LEITURA
}
```

