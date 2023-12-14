import json
import time
import grpc
import uuid
from api import robotskill_pb2
from api import robotskill_pb2_grpc
from handle_data import HandleData

id = [
    "reportLocation",
    "reportStatus",
    "robotStatus",
    "reportMapList",
    "reportRmfRoute",
    "reportEvent"
]


class GrpcCross(object):
    def __init__(self):
        self.host = "172.16.13.134:32403"
        self.channel = grpc.insecure_channel(self.host)
        self.stub = robotskill_pb2_grpc.RobotSkillServiceStub(self.channel)
        self.guid = str(uuid.uuid4().hex)

        self.robot_id = "GINLITXR-1LXXXXXXXXXGNL01S2046000001"
        self.tenant_id = "peter10"
        self.robot_type = "Cloud Ginger-Lite"
        self.service_code = "gingerlite"
        self.user_id = "GNL01S2046000001"  # roc user_id
        self.message_id = "reportLocation"

    # 技能请求
    # def grpc_enable_skill_test(self):
    #     timestamp = str(int(time.time() * 1000))
    #     skill_request = robotskill_pb2.EnableSkillRequest(
    #         common_req_info=robotskill_pb2.common.CommonReqInfo(
    #             guid=self.guid,
    #             timestamp=timestamp,
    #             version="",
    #             tenant_id=self.tenant_id,
    #             user_id=self.user_id,
    #             robot_id=self.robot_id,
    #             robot_type=self.robot_type,
    #             service_code=self.service_code,
    #             seq="",
    #             root_guid=""
    #         ),
    #         ability=True,  # true to subscribe, false unsubscribe
    #         param="",
    #         sub_addr="",  # subscriber gRPC address
    #         sub_name="",  # subscriber name, the same subscriber should use fixed name
    #         extra_type=""  # optional, use for sub suffix,max length no more than 64, align to common.Extra.extra_type.
    #     )
    #     response = self.stub.EnableSkill(skill_request)
    #     return response

    # handle action
    def grpc_handle_action_test(self):
        timestamp = int(time.time() * 1000)
        action_request = robotskill_pb2.ActionRequest(
            common_req_info=robotskill_pb2.api_dot_common_dot_common__pb2.CommonReqInfo(
                guid=self.guid,
                timestamp=timestamp,
                version="v1.2",  # 随便填
                tenant_id=self.tenant_id,
                user_id=self.user_id,  # roc user id
                robot_id=self.robot_id,
                robot_type=self.robot_type,
                service_code=self.service_code,
                seq="",  # null
                root_guid=""  # null
            ),
            id=self.message_id,  # 消息类型      reportLocation   类型 和 param 以及 context如何对应
            param=json.dumps(HandleData().get_param_data(self.message_id)),  # 消息相关数据   json 串
            context=""  # 技能上下文   不写
        )
        response = self.stub.HandleAction(action_request)
        res = {
            "data": response.data,
            "common_resp_info": {
                "err_code": response.common_resp_info.err_code,
                "err_msg": response.common_resp_info.err_msg,
                "err_detail": response.common_resp_info.err_detail}
        }
        return res


if __name__ == '__main__':
    # 让开发给个示例
    cross = GrpcCross()
    time0 = time.time()
    for index in range(5):
        message = cross.grpc_handle_action_test()
        print(message)
    print(f"Elapsed time: {time.time()-time0}s")
