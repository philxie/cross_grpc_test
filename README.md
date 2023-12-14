python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. helloworld.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. api/common/*.proto

## 单实例
locust -f utils/locust_talk.py -u 2 -t 3m -H 172.16.13.135:31359 --headless --html reports/talk2309222159.html --test-config testsuite/smartvoice/intent/intent_sv_talk_136.json
locust -f locustfile.py -u 50 -t 1m -H 172.16.13.134:32403 --headless --html reports/cross202309232351.html
locust -f locustfile.py -u 200 -t 1m -H 172.16.13.134:32403 --headless --html reports/cross202309232351.html
locust -f locustfile.py -u 62500 -r 500 -t 10m -H 172.16.13.134:32403 --headless --html reports/cross202309242020.html
locust -f locustfile.py -u 600 -r 1 -t 10h -H 172.16.13.134:32403 --headless --html reports/cross202309242230.html

在非Web UI下运行Locust分布式
当开始启动master节点时要指定--expect-workers参数来指定worker节点的连接数量
默认情况下，locust将立即停止任务（甚至不等待请求完成）。如果要允许任务完成其迭代，则可以使用
```powershell
locust --headless --run-time 1h30m --stop-timeout 10

locust --master --headless --expect-workers=1 --html reports/cross202309242336.html
locust --worker --master-host=10.12.32.121
```
locust --headless --html reports/cross202309242230.html

locust --master --headless --expect-workers=2 --html reports/cross202309242336.html
locust --worker --master-host=10.12.32.121
locust --worker --master-host=10.12.32.121`

## 三实例测试
预计user数可达到1500个，最大2000个
locust -f locustfile.py --headless --html reports/202310272200_robotskill.html
# 10.10.50.201 服务器本地复测
locust -f locustfile.py --headless --html reports/202312092231_robotskill.html