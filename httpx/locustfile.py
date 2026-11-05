from locust import HttpUser, task, between


class DeviceUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_all_devices(self):
        self.client.get("/devices")

    @task(2)
    def get_single_device(self):
        self.client.get("/devices/1")

    @task(1)
    def create_and_delete_device(self):
        # Create
        response = self.client.post(
            "/devices",
            json={
                "name": "LoadTestDevice",
                "status": "Active",
                "owner": "Locust"
            }
        )
        if response.status_code == 201:
            device_id = response.json().get("id")
            # Delete cleanup
            self.client.delete(f"/devices/{device_id}")