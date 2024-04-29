# Use a imagem oficial do Python 3.11 como base
FROM python:3.11

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o código fonte da aplicação para o contêiner
COPY . /app

# Instale as dependências Python
RUN pip install Flask cryptography==40.0.2

# Exponha a porta que a aplicação irá escutar (se necessário)
EXPOSE 5005
EXPOSE 12345
EXPOSE 12346

# Comando para executar a aplicação
CMD ["python", "api.py"]
