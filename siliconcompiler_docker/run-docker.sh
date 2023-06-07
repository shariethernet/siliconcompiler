#!/bin/bash
# Mounts silicon compiler repo as a docker volume and builds docker image

set -e

DOCKER_GID=$(id -g)
DOCKER_GNAME=$(id -gn)
DOCKER_UNAME=$(id -un)
DOCKER_UID=$(id -u)
DOCKER_TAG=$DOCKER_UNAME/siliconcompiler:$(date +%Y%m%d%H%M)
SILICONCOMPILER_PATH=$(readlink -f $(dirname ${0})/../)
SILICONCOMPILER_MOUNT_POINT=/workspace/siliconcompiler

docker build \
    -t ${DOCKER_TAG} \
    -f siliconcompiler_docker/Dockerfile.cpu \
    .

DOCKER_EXEC="docker run --rm --shm-size 32G -i -t --init "

echo "Mounting  ${SILICONCOMPILER_PATH} to ${SILICONCOMPILER_MOUNT_POINT} inside the docker container"
DOCKER_EXEC+="-v ${SILICONCOMPILER_PATH}:${SILICONCOMPILER_MOUNT_POINT} "
DOCKER_EXEC+="-v /home/local/nu/shg/tiny_aes:/workspace/tiny_aes "
DOCKER_EXEC+="-e DISPLAY=$DISPLAY "
DOCKER_EXEC+="-v /tmp/.X11-unix/:/tmp/.X11-unix/ "
DOCKER_EXEC+="${DOCKER_TAG} /bin/bash"

$DOCKER_EXEC

