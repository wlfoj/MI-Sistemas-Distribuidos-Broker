# Use a imagem oficial do Python 3.11 como base
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o código fonte da aplicação para o contêiner
COPY . /app

# Instale as dependências Python
#RUN pip install Flask cryptography==40.0.2 Flask-Caching
RUN pip install -r requirements.txt
# Exponha a porta que a aplicação irá escutar (se necessário)
# Porta da API Restfull
EXPOSE 5005 

# Comando para executar a aplicação
CMD ["python", "api.py"]
