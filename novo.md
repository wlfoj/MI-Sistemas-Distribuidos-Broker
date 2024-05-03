docker pull wolivej/middleware_b_i:latest
docker pull wolivej/device_i:latest


# Execute device
docker run -p 12345:12345 -p 12346:12346 -it wolivej/device_i
# Execute broker
docker run -p 12345:12345 -p 12346:12346 -p 5005:5005 -it wolivej/middleware_b_i


# Fazendo a imagem no dockerHUB
docker build -t wolivej/device_i:latest .
docker push wolivej/device_i:latest


docker build -t wolivej/middleware_b_i:latest .
docker push wolivej/middleware_b_i:latest