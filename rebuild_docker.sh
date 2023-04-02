echo STOPPING PONG BOT..
docker stop FCFB-Pong-Bot
echo PONG BOT STOPPED!
echo
echo REMOVING OLD PONG BOT...
docker remove FCFB-Pong-Bot
echo OLD PONG BOT REMOVED!
echo
echo BUILDING NEW PONG BOT...
docker build -t "fcfb-pong-bot:Dockerfile" .
echo NEW PONG BOT BUILT!
echo
echo STARTING NEW PONG BOT...
docker run -d --restart=always --name FCFB-Pong-Bot fcfb-pong-bot:Dockerfile
echo NEW PONG BOT STARTED!
echo DONE!
