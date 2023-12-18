# coding: utf8

import six
from itertools import chain
import os
# os.system("tail -f /dev/null")

from flask import request, Response
from locust import stats as locust_stats, runners as locust_runners
# from locust import User, task, events
from locust import task, events, run_single_user, constant, between, LoadTestShape, tag
import grpc_user
from prometheus_client import Metric, REGISTRY, exposition

# This locustfile adds an external web endpoint to the locust master, and makes it serve as a prometheus exporter.
# Runs it as a normal locustfile, then points prometheus to it.
# locust -f prometheus_exporter.py --master

# Lots of code taken from [mbolek's locust_exporter](https://github.com/mbolek/locust_exporter), thx mbolek!


class LocustCollector(object):
    registry = REGISTRY

    def __init__(self, environment, runner):
        self.environment = environment
        self.runner = runner

    def collect(self):
        # collect metrics only when locust runner is spawning or running.
        runner = self.runner

        if runner and runner.state in (locust_runners.STATE_SPAWNING, locust_runners.STATE_RUNNING):
            stats = []
            for s in chain(locust_stats.sort_stats(runner.stats.entries), [runner.stats.total]):
                stats.append({
                    "method": s.method,
                    "name": s.name,
                    "num_requests": s.num_requests,
                    "num_failures": s.num_failures,
                    "avg_response_time": s.avg_response_time,
                    "min_response_time": s.min_response_time or 0,
                    "max_response_time": s.max_response_time,
                    "current_rps": s.current_rps,
                    "median_response_time": s.median_response_time,
                    "ninetieth_response_time": s.get_response_time_percentile(0.9),
                    # only total stats can use current_response_time, so sad.
                    #"current_response_time_percentile_95": s.get_current_response_time_percentile(0.95),
                    "avg_content_length": s.avg_content_length,
                    "current_fail_per_sec": s.current_fail_per_sec
                })

            # perhaps StatsError.parse_error in e.to_dict only works in python slave, take notices!
            errors = [e.to_dict() for e in six.itervalues(runner.stats.errors)]

            metric = Metric('locust_user_count', 'Swarmed users', 'gauge')
            metric.add_sample('locust_user_count', value=runner.user_count, labels={})
            yield metric
            
            metric = Metric('locust_errors', 'Locust requests errors', 'gauge')
            for err in errors:
                metric.add_sample('locust_errors', value=err['occurrences'],
                                  labels={'path': err['name'], 'method': err['method'],
                                          'error': err['error']})
            yield metric

            is_distributed = isinstance(runner, locust_runners.MasterRunner)
            if is_distributed:
                metric = Metric('locust_slave_count', 'Locust number of slaves', 'gauge')
                metric.add_sample('locust_slave_count', value=len(runner.clients.values()), labels={})
                yield metric

            metric = Metric('locust_fail_ratio', 'Locust failure ratio', 'gauge')
            metric.add_sample('locust_fail_ratio', value=runner.stats.total.fail_ratio, labels={})
            yield metric

            metric = Metric('locust_state', 'State of the locust swarm', 'gauge')
            metric.add_sample('locust_state', value=1, labels={'state': runner.state})
            yield metric

            stats_metrics = ['avg_content_length', 'avg_response_time', 'current_rps', 'current_fail_per_sec',
                             'max_response_time', 'ninetieth_response_time', 'median_response_time', 'min_response_time',
                             'num_failures', 'num_requests']

            for mtr in stats_metrics:
                mtype = 'gauge'
                if mtr in ['num_requests', 'num_failures']:
                    mtype = 'counter'
                metric = Metric('locust_stats_' + mtr, 'Locust stats ' + mtr, mtype)
                for stat in stats:
                    # Aggregated stat's method label is None, so name it as Aggregated
                    # locust has changed name Total to Aggregated since 0.12.1
                    if 'Aggregated' != stat['name']:
                        metric.add_sample('locust_stats_' + mtr, value=stat[mtr],
                                          labels={'path': stat['name'], 'method': stat['method']})
                    else:
                        metric.add_sample('locust_stats_' + mtr, value=stat[mtr],
                                          labels={'path': stat['name'], 'method': 'Aggregated'})
                yield metric


@events.init.add_listener
def locust_init(environment, runner, **kwargs):
    print("locust init event received")
    if environment.web_ui and runner:
        @environment.web_ui.app.route("/export/prometheus")
        def prometheus_exporter():
            registry = REGISTRY
            encoder, content_type = exposition.choose_encoder(request.headers.get('Accept'))
            if 'name[]' in request.args:
                registry = REGISTRY.restricted_registry(request.args.get('name[]'))
            body = encoder(registry)
            return Response(body, content_type=content_type)
        REGISTRY.register(LocustCollector(environment, runner))


# 基于时间段负载策略：前10s和10-20s用户数为10；20-50s用户数为50；50-80s用户数为100；80s后用户数为30
# class TimeStageShape():
class TimeStageShape(LoadTestShape):
    """
        duration -- 多少秒后进入下一个阶段
        users -- 用户数
        spawn_rate -- 每秒要启动/停止的用户数
    """
    stages = [
        {"duration": 300, "users": 1, "spawn_rate": 1},
        {"duration": 600, "users": 100, "spawn_rate": 10},
        {"duration": 900, "users": 200, "spawn_rate": 10},
        {"duration": 1200, "users": 400, "spawn_rate": 10},
        {"duration": 1800, "users": 500, "spawn_rate": 10},
        {"duration": 2400, "users": 600, "spawn_rate": 10},
        {"duration": 3000, "users": 700, "spawn_rate": 10},
        {"duration": 3600, "users": 800, "spawn_rate": 10},
        {"duration": 4200, "users": 900, "spawn_rate": 10},
        {"duration": 4800, "users": 1000, "spawn_rate": 10},
        {"duration": 5400, "users": 1100, "spawn_rate": 10},
        {"duration": 6000, "users": 1150, "spawn_rate": 10},
        {"duration": 6600, "users": 1200, "spawn_rate": 10},
        {"duration": 7200, "users": 1250, "spawn_rate": 10},
        {"duration": 7800, "users": 1300, "spawn_rate": 10},
        {"duration": 8400, "users": 1350, "spawn_rate": 10},
        {"duration": 9000, "users": 1400, "spawn_rate": 10},
        {"duration": 9600, "users": 1450, "spawn_rate": 10},
        {"duration": 10200, "users": 1500, "spawn_rate": 10},
        {"duration": 10800, "users": 1550, "spawn_rate": 10},
        {"duration": 11400, "users": 1600, "spawn_rate": 10},
        {"duration": 12000, "users": 1650, "spawn_rate": 10},
        {"duration": 12600, "users": 1700, "spawn_rate": 10},
        {"duration": 13200, "users": 1750, "spawn_rate": 10},
        {"duration": 13800, "users": 1800, "spawn_rate": 10},
        {"duration": 14400, "users": 1850, "spawn_rate": 10},
        {"duration": 15000, "users": 1900, "spawn_rate": 10},
        {"duration": 15600, "users": 1950, "spawn_rate": 10},
        {"duration": 16200, "users": 2000, "spawn_rate": 10},

        {"duration": 16800, "users": 1900, "spawn_rate": 10},
        {"duration": 17400, "users": 1800, "spawn_rate": 10},
        {"duration": 18000, "users": 1700, "spawn_rate": 10},
        {"duration": 18600, "users": 1600, "spawn_rate": 10},
        {"duration": 19200, "users": 1500, "spawn_rate": 10},
        {"duration": 19800, "users": 1400, "spawn_rate": 10},
        {"duration": 20400, "users": 1300, "spawn_rate": 10},
        {"duration": 21000, "users": 1200, "spawn_rate": 10},
        {"duration": 21600, "users": 1100, "spawn_rate": 10},
        {"duration": 22200, "users": 1000, "spawn_rate": 10},
        {"duration": 22800, "users": 900, "spawn_rate": 10},
        {"duration": 23400, "users": 800, "spawn_rate": 10},
        {"duration": 24000, "users": 700, "spawn_rate": 10},
        {"duration": 24600, "users": 600, "spawn_rate": 10},
        {"duration": 25200, "users": 500, "spawn_rate": 10},
        {"duration": 25800, "users": 400, "spawn_rate": 10},
        {"duration": 26400, "users": 300, "spawn_rate": 10},
        {"duration": 27000, "users": 200, "spawn_rate": 10},
        {"duration": 27600, "users": 100, "spawn_rate": 10},
        {"duration": 28200, "users": 1, "spawn_rate": 10},
    ]
    time_limit = 36000

    def tick(self):
        # 调用get_run_time()方法获取压测执行的时间
        run_time = self.get_run_time()

        for stage in self.stages:
            # 判断运行时间在不同阶段负载不同用户数量
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
            # 设置运行总时间
            elif self.stages[-1]["duration"] < run_time < self.time_limit:
                tick_data = (self.stages[-1]["users"], self.stages[-1]["spawn_rate"])
                return tick_data

        return None
    

class Dummy(grpc_user.GrpcUser):
    @task(20)
    def hello(self):
        pass
