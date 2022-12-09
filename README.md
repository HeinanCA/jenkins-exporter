# Jenkins Exporter

[![Build Status](https://travis-ci.org/akawork/Jenkins-exporter.svg?branch=master)](https://travis-ci.org/akawork/Jenkins-exporter)

Jenkins exporter is a exporter to get metrics of Jenkins server, deployed on FSOFT environment.

Jenkins exporter has been written in python3. It's tested in Jenkins version 2.143 and 2.176.1.

*Note: We used **timestamp()** in **datetime** library not supported by python2, so make sure running Jenkins exporter in python3 or newer*

## Usage:

You can download source code and build docker yourself, or use docker image we have built.

### Step 1: Build image

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
-e "PROM_EXPORTER_PORT=9118" jenkins_exporter
```

With:

- JENKINS_SERVER: is the url of Jenkins
- JENKINS_HTTPS_INSECURE: true for self-signed certificates, false for valid ones
- JENKINS_USERNAME: is the user of Jenkins who have permission to access Jenkins resource
- JENKINS_PASSWORD: is the password of user
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
JENKINS_SERVER = http://jenkins_server:8080
JENKINS_HTTPS_INSECURE = true
JENKINS_USERNAME = username
JENKINS_PASSWORD = password
```
