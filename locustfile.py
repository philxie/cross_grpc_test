from locust import HttpUser, task, between

class Dummy(HttpUser):
    wait_time = between(1, 2)

    @task
    def index(self):
        self.client.get("/")
        