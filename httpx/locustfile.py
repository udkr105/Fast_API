
from locust import HttpUser, task, between


# Define a virtual user
class DeviceUser(HttpUser):

    # Wait between 1 and 3 seconds
    # before executing the next task
    wait_time = between(1, 3)

    # Task 1: Get all devices
    @task(3)
    def get_all_devices(self):

        with self.client.get(
            "/devices",
            name="GET /devices",
            catch_response=True
        ) as response:

            if response.status_code == 200:

                data = response.json()

                if isinstance(data, list):
                    response.success()
                else:
                    response.failure(
                        "Expected a list in response"
                    )

            else:
                response.failure(
                    f"Unexpected status: {response.status_code}"
                )


    # Task 2: Get device by ID
    @task(1)
    def get_device_by_id(self):

        with self.client.get(
            "/devices/1",
            name="GET /devices/{id}",
            catch_response=True
        ) as response:

            if response.status_code == 200:

                data = response.json()

                if data.get("id") == 1:
                    response.success()
                else:
                    response.failure(
                        "Incorrect device ID"
                    )

            else:
                response.failure(
                    f"Unexpected status: {response.status_code}"
                )
