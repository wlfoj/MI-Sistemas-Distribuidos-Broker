# Use a imagem oficial do Python 3.11 como base
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o código fonte da aplicação para o contêiner
COPY . /app

# Instale as dependências Python
RUN pip install cryptography==40.0.2

# Exponha a porta que a aplicação irá escutar (se necessário)

# Comando para executar a aplicação
# CMD ["python", "main.py"]
CMD ["/bin/bash"]
