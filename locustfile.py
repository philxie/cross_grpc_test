from locust import HttpUser, task, between

class Dummy(HttpUser):
    wait_time = between(2, 5)

    @task
    def index(self):
        self.client.get("/")
        