import os
import sys
import time
import configparser
from socket import gaierror
from urllib3.exceptions import NewConnectionError
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from jenkins.jenkins import JenkinsCollector

if __name__ == "__main__":
    # Import configuration file, if present
    config = configparser.ConfigParser()
    config.read(os.getenv('CONFIG_FILE_PATH', "config.ini"))

    # If no environment values are provided, get it from config file
    jenkins_config = {}
    jenkins_config["server"] = os.getenv('JENKINS_SERVER', config.get('DEFAULT', 'JENKINS_SERVER', fallback=None))
    jenkins_config["insecure"] = bool(os.getenv('JENKINS_HTTPS_INSECURE',
                                                config.get('DEFAULT', 'JENKINS_HTTPS_INSECURE', fallback=None)))
    jenkins_config["user"] = os.getenv('JENKINS_USERNAME', config.get('DEFAULT', 'JENKINS_USERNAME', fallback=None))
    jenkins_config["passwd"] = os.getenv('JENKINS_PASSWORD', config.get('DEFAULT', 'JENKINS_PASSWORD', fallback=None))

    prometheus_config = {}
    prometheus_config["port"] = int(os.getenv('PROM_EXPORTER_PORT', 9118))
    prometheus_config["metric_types"] = os.getenv('PROM_METRIC_TYPES', 
                                                  config.get('DEFAULT', 'PROM_METRIC_TYPES', fallback="all"))

    collector = JenkinsCollector(metric_types=prometheus_config["metric_types"], **jenkins_config)
    try:
        REGISTRY.register(collector)
        start_http_server(prometheus_config["port"])
        while True:
            time.sleep(1)
    except (gaierror, NewConnectionError, MaxRetryError, ConnectionError):
        print(f"Couldn't connect to server {jenkins_config['server']}, please check your configuration.")
        exit(111)
