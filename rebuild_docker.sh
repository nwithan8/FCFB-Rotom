echo STOPPING ROTOM BOT..
docker stop FCFB-Rotom
echo ROTOM BOT STOPPED!
echo
echo REMOVING OLD ROTOM BOT...
docker remove FCFB-Rotom
echo OLD ROTOM BOT REMOVED!
echo
echo BUILDING NEW ROTOM BOT...
docker build -t "fcfb-rotom:Dockerfile" .
echo NEW ROTOM BOT BUILT!
echo
echo STARTING NEW ROTOM BOT...
docker run -d --restart=always --name FCFB-Rotom fcfb-rotom:Dockerfile
echo NEW ROTOM BOT STARTED!
echo DONE!