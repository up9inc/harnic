#!/bin/bash -xe

docker pull gcr.io/mimetic-card-241611/harnic/develop
docker build .. -f ../Dockerfile.demo -t jenkins
docker run -it -p 8080:8080 -v `pwd`/jenkins-data:/var/jenkins_home jenkins
# -v /var/run/docker.sock:/var/run/docker.sock
