# Define the Docker image name
DOCKER_IMAGE_NAME="fcfb-rotom:Dockerfile"
CONTAINER_NAME="FCFB-Rotom"

# Check if the Docker container is running
if docker ps -q --filter "name=${CONTAINER_NAME}" | grep -q .; then
    echo "STOPPING ROTOM BOT..."
    docker stop ${CONTAINER_NAME}
    echo "ROTOM BOT STOPPED!"
    echo

    echo "REMOVING OLD ROTOM BOT..."
    docker rm ${CONTAINER_NAME}
    echo "OLD ROTOM BOT REMOVED!"
    echo
else
    echo "ROTOM BOT is not running. No need to stop and remove."
    echo
fi

echo "BUILDING NEW ROTOM BOT..."
docker build -t "${DOCKER_IMAGE_NAME}" --build-arg CONFIG_FILE=config.json .
echo "NEW ROTOM BOT BUILT!"
echo

echo "STARTING NEW ROTOM BOT..."
docker run -d --restart=always --name ${CONTAINER_NAME} ${DOCKER_IMAGE_NAME}
echo "NEW ROTOM BOT STARTED!"
echo "DONE!"

docker system prune -a --force