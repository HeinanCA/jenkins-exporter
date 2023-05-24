# Jenkins Exporter

[![Docker Image CI](https://github.com/HeinanCA/jenkins-exporter/actions/workflows/docker-image.yml/badge.svg)](https://github.com/HeinanCA/jenkins-exporter/actions/workflows/docker-image.yml)

Jenkins exporter is an exporter to get metrics of Jenkins server, deployed on FSOFT environment.

Jenkins exporter has been written in python3. It's been tested with Jenkins versions 2.143, 2.176.1 and 2.332.2, 2.387.3

*Note: Supported Python versions are Python 3.11.x, so make sure you are running Jenkins Exporter with those versions*

## Usage:

You can download the source code and build docker yourself, or use the docker image under the Docker Hub repository: https://hub.docker.com/r/heinanca/jenkins-exporter

### Step 1: Build an image

```sh
docker build -t jenkins_exporter .
```

### Step 2: Run Jenkins exporter

```sh
docker run -p 9118:9118 --name jenkins_exporter -d \
-e "JENKINS_SERVER=https://jenkins_server" \
-e "JENKINS_HTTPS_INSECURE=true" \
-e "JENKINS_USERNAME=example" \
-e "JENKINS_PASSWORD=123456" \
-e "PROM_METRIC_TYPES=node,queue" \
-e "PROM_EXPORTER_PORT=9118" jenkins_exporter
```

With:

- JENKINS_SERVER: is the URL of Jenkins
- JENKINS_HTTPS_INSECURE: true for self-signed certificates, false for valid ones
- JENKINS_USERNAME: is the user of Jenkins who has permission to access Jenkins resource
- JENKINS_PASSWORD: is the password of the user
- PROM_METRIC_TYPES: a comma-separated list of metric types you would like to see, e.g. "job, node,queue" or simply "all"
- PROM_EXPORTER_PORT: the port where the exporter will listen.

### *Or using config file:*
```sh
docker run -p 9118:9118 --name jenkins_exporter -d \
-v "/link/to/your/jenkins/config/file.ini:/root/config.ini" \
-e "PROM_EXPORTER_PORT=9118" jenkins_exporter
```

with ***config.ini:***
```ini
[DEFAULT]
JENKINS_SERVER=http://jenkins_server:8080
JENKINS_HTTPS_INSECURE=true
JENKINS_USERNAME=username
JENKINS_PASSWORD=password
PROM_METRIC_TYPES=all
```
