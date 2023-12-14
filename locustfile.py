#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import threading
import jsonlines as jsonlines
import json

from handle_data import HandleData
from datetime import datetime as dt
import time
import uuid
import grpc
import pandas as pd
from api import robotskill_pb2, robotskill_pb2_grpc
from locust import task, events, run_single_user, constant, between, LoadTestShape, tag
import grpc_user


def get_robot_ids(csv_file=r"robot_ids.csv"):
    """
    获取robotId列表
    @param csv_file:
    @return:
    """

    df = pd.read_csv(os.path.join(os.getcwd(), "testdata", csv_file))
    robot_ids = df.values.tolist()
    return robot_ids


_today = dt.now().strftime("%Y%m%d%H%M%S")
logs_path = f"logs/{_today}.jsonl"


def mock_trace_id():
    return str(uuid.uuid4()) + "@cloudminds-test.com.cn"


# 基于时间段负载策略：前10s和10-20s用户数为10；20-50s用户数为50；50-80s用户数为100；80s后用户数为30
# class TimeStageShape():
class TimeStageShape(LoadTestShape):
    """
        duration -- 多少秒后进入下一个阶段
        users -- 用户数
        spawn_rate -- 每秒要启动/停止的用户数
    """
    stages = [
        {"duration": 600, "users": 300, "spawn_rate": 10},
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

        {"duration": 16800, "users": 1700, "spawn_rate": 10},
        {"duration": 17400, "users": 1400, "spawn_rate": 10},
        {"duration": 18000, "users": 1100, "spawn_rate": 10},
        {"duration": 18600, "users": 800, "spawn_rate": 10},
        {"duration": 19200, "users": 500, "spawn_rate": 10},
        {"duration": 19800, "users": 300, "spawn_rate": 10},
        {"duration": 20400, "users": 200, "spawn_rate": 10},
        {"duration": 21000, "users": 100, "spawn_rate": 10},
        {"duration": 21600, "users": 50, "spawn_rate": 10},
        {"duration": 22200, "users": 10, "spawn_rate": 10},
        {"duration": 22800, "users": 1, "spawn_rate": 10}
    ]

    stages_1 = [
        {"duration": 300, "users": 300, "spawn_rate": 10},
        {"duration": 600, "users": 400, "spawn_rate": 10},
        {"duration": 900, "users": 450, "spawn_rate": 10},
        {"duration": 1200, "users": 500, "spawn_rate": 10},
        {"duration": 1800, "users": 550, "spawn_rate": 10},
        {"duration": 3600, "users": 600, "spawn_rate": 10},
        {"duration": 5400, "users": 650, "spawn_rate": 10},
        {"duration": 7200, "users": 700, "spawn_rate": 10},
        {"duration": 9000, "users": 750, "spawn_rate": 10},
        {"duration": 10800, "users": 800, "spawn_rate": 10},
        {"duration": 12600, "users": 850, "spawn_rate": 10},
        {"duration": 14400, "users": 900, "spawn_rate": 10},
        {"duration": 16200, "users": 950, "spawn_rate": 10},
        {"duration": 18000, "users": 1000, "spawn_rate": 10},
        {"duration": 19800, "users": 1100, "spawn_rate": 10},
        {"duration": 21600, "users": 1200, "spawn_rate": 10},
        {"duration": 23400, "users": 1300, "spawn_rate": 10},
        {"duration": 25200, "users": 1400, "spawn_rate": 10},
        {"duration": 27000, "users": 1500, "spawn_rate": 10},
        {"duration": 28800, "users": 1600, "spawn_rate": 10}
    ]
    stages_0 = [
        {"duration": 1800, "users": 50, "spawn_rate": 5},
        {"duration": 3600, "users": 100, "spawn_rate": 5},
        {"duration": 5400, "users": 150, "spawn_rate": 5},
        {"duration": 7200, "users": 200, "spawn_rate": 5},
        {"duration": 9000, "users": 250, "spawn_rate": 5},
        {"duration": 10800, "users": 300, "spawn_rate": 5},
        {"duration": 12600, "users": 350, "spawn_rate": 5},
        {"duration": 14400, "users": 400, "spawn_rate": 5},
        {"duration": 16200, "users": 450, "spawn_rate": 5},
        {"duration": 18000, "users": 500, "spawn_rate": 5}

        # {"duration": 19800, "users": 550, "spawn_rate": 5},
        # {"duration": 21600, "users": 600, "spawn_rate": 5},
        # {"duration": 23400, "users": 650, "spawn_rate": 5},
        # {"duration": 25200, "users": 700, "spawn_rate": 5},
        # {"duration": 27000, "users": 750, "spawn_rate": 5},
        # {"duration": 28800, "users": 800, "spawn_rate": 5}
    ]
    time_limit = 23000

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


class GrpcTask(grpc_user.GrpcUser):
    # interceptor = StreamStreamGrpcInterceptor
    stub_class = robotskill_pb2_grpc.RobotSkillServiceStub

    host = "172.16.13.134:32403"
    channel = grpc.insecure_channel(host)
    stub = robotskill_pb2_grpc.RobotSkillServiceStub(channel)

    robot_id = "GINLITXR-1LXXXXXXXXXGNL01S2046000001"
    tenant_id = "peter10"
    robot_type = "Cloud Ginger-Lite"
    service_code = "gingerlite"
    user_id = "GNL01S2046000001"  # roc user_id
    message_id = "reportLocation"

    def on_start(self):
        logging.info("*********START TEST***********")

    def on_stop(self):
        logging.info("*********STOP TEST***********")

    @task
    @tag("task")
    def connect(self):
        # ------------------------------
        timestamp = int(time.time() * 1000)
        guid = str(uuid.uuid4().hex)
        res = {}
        req = {
            "guid": guid,
            "timestamp": timestamp,
            "version": "v1.2",
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,  # roc user id
            "robot_id": self.robot_id,
            "robot_type": self.robot_type,
            "service_code": self.service_code,
            "id": self.message_id,
            "param": json.dumps(HandleData().get_param_data(self.message_id))
        }
        try:
            action_request = robotskill_pb2.ActionRequest(
                common_req_info=robotskill_pb2.api_dot_common_dot_common__pb2.CommonReqInfo(
                    guid=guid,
                    timestamp=timestamp,
                    version="v1.2",  # 随便填
                    tenant_id=self.tenant_id,
                    user_id=self.user_id,  # roc user id
                    robot_id=self.robot_id,
                    robot_type=self.robot_type,
                    service_code=self.service_code,
                    seq="",       # null
                    root_guid=""  # null
                ),
                id=self.message_id,  # 消息类型      reportLocation   类型 和 param 以及 context如何对应
                param=json.dumps(HandleData().get_param_data(self.message_id)),  # 消息相关数据   json 串
                context=""      # 技能上下文   不写
            )
            response = self.stub.HandleAction(action_request)
            interface_time = int(time.time() * 1000) - timestamp
            # res = {
            #     "data": response.data,
            #     "common_resp_info": {
            #         "err_code": response.common_resp_info.err_code,
            #         "err_msg": response.common_resp_info.err_msg,
            #         "err_detail": response.common_resp_info.err_detail}
            # }
            if "success" != response.common_resp_info.err_msg:
                raise Exception(f"response error:{response}")
        except Exception as e:
            interface_time = int(time.time() * 1000) - timestamp
            events.request.fire(request_type="grpc",
                                name=self.host,
                                response_time=interface_time,
                                context="",
                                response_length=len(str(e)),
                                exception=e)
            print(e)
            with threading.Lock():
                with jsonlines.open(logs_path, "a") as jf:
                    jf.write({
                        "req": req,
                        "res": str(e)
                    })
        else:  # no exception
            events.request.fire(request_type="grpc",
                                name=self.host,
                                response_time=interface_time,
                                context="",
                                response_length=50,
                                exception=Exception(f"response cost:{interface_time} >= 60000 ms") if interface_time >= 60000 else None)

        # finally:
        #     with threading.Lock():
        #         with jsonlines.open(logs_path, "a") as jf:
        #             jf.write({
        #                 "req": req,
        #                 "res": res
        #             })
        #     # total_time = int((time.time() - start_time) * 1000)
        #     # logging.info(f"interface_time={interface_time}, total_time={total_time}")
        #     # print(f"{datetime.now()}: interface_time={interface_time}, total_time={total_time}")
        #     # data = pd.DataFrame({"RT": total_time})
        #     # data.to_csv('data.csv', sep=',')
        #
        #     with threading.Lock():
        #         with jsonlines.open(logs_path, "a") as jf:
        #             jf.write(res)


if __name__ == '__main__':
    # run_single_user({"SchemaGrpcTask": 10, "TtsGrpcTask": 3})
    run_single_user(GrpcTask)
