import os
import sys

from jenkins.data.jobs import Jobs
from jenkins.data.queue import Queue
from jenkins.data.nodes import Nodes
from jenkins.metrics import job_metrics, node_metrics, queue_metrics
from jenkins.connection.api_connection import APIConnection


class Jenkins(object):

    def __init__(self, server, auth, insecure=True):
        self.server = server
        self.auth = auth
        self.req = APIConnection(server, auth, insecure)
        self.jobs = Jobs(self)
        self.queue = Queue(self)
        self.nodes = Nodes(self)


class JenkinsCollector(object):

    def __init__(self, server, user, passwd, insecure=False, metric_types="job,node,queue"):
        self.server = server
        self.insecure = insecure
        self.auth = (user, passwd)
        self.metric_types = metric_types.split(",")

    def collect(self):
        jenkins = Jenkins(
            server=self.server,
            auth=self.auth,
            insecure=self.insecure
        )

        jenkins_metrics = JenkinsMetrics(jenkins, self.metric_types)
        metrics = jenkins_metrics.make_metrics()

        for metric in metrics:
            yield metric


class JenkinsMetrics(object):

    def __init__(self, jenkins, metric_types):
        self.jenkins = jenkins
        self.metrics = []
        self.metric_types= metric_types

    def make_metrics(self):
        metrics = []

        if ("job" in self.metric_types or "all" in self.metric_types):
            metrics += job_metrics.make_metrics(self.jenkins.jobs)
        if ("node" in self.metric_types or "all" in self.metric_types):
            metrics += node_metrics.make_metrics(self.jenkins.nodes)
        if ("queue" in self.metric_types or "all" in self.metric_types):
            metrics += queue_metrics.make_metrics(self.jenkins.queue)

        self.metrics = metrics

        return self.metrics
