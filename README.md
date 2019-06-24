# Docker-Directory

A simple web app showing what Docker containers are running on the server

For when you run a bunch of docker containers on some server in the closet and they listen on some ports and then you forget where you put things and don't want to SSH onto the server.

## Running

```
docker run -d --name directory -p 80:80 -v /var/run/docker.sock:/var/run/docker.sock:ro waisbrot/docker-directory
```
