docker stop FCFB-Pong-Bot
docker remove FCFB-Pong-Bot
docker build -t "fcfb-pong-bot:Dockerfile" .
docker run -d --restart=always --name FCFB-Pong-Bot fcfb-pong-bot:Dockerfile
