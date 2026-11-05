from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Devices Management API")


# Request body model
class Device(BaseModel):
    name: str
    status: str
    owner: str


# In-memory database
devices = [
    {
        "id": 1,
        "name": "Laptop",
        "status": "Active",
        "owner": "Irfan"
    },
    {
        "id": 2,
        "name": "Desktop",
        "status": "Inactive",
        "owner": "Rahul"
    }
]


# Health check API
@app.get("/")
def home():
    return {"message": "Devices API is running"}


# GET: Retrieve all devices
@app.get("/devices")
def get_devices():
    return devices


# GET: Retrieve device by ID
@app.get("/devices/{device_id}")
def get_device(device_id: int):
    for device in devices:
        if device["id"] == device_id:
            return device

    raise HTTPException(
        status_code=404,
        detail="Device not found"
    )


# POST: Create a new device
@app.post("/devices", status_code=status.HTTP_201_CREATED)
def create_device(device: Device):
    new_id = max(
        [d["id"] for d in devices],
        default=0
    ) + 1

    new_device = {
        "id": new_id,
        **device.model_dump()
    }

    devices.append(new_device)
    return new_device


# PUT: Update an existing device
@app.put("/devices/{device_id}")
def update_device(device_id: int, updated_device: Device):
    for device in devices:
        if device["id"] == device_id:
            device.update(updated_device.model_dump())
            return device

    raise HTTPException(
        status_code=404,
        detail="Device not found"
    )


# DELETE: Delete a device
@app.delete("/devices/{device_id}", status_code=204)
def delete_device(device_id: int):
    for device in devices:
        if device["id"] == device_id:
            devices.remove(device)
            return

    raise HTTPException(
        status_code=404,
        detail="Device not found"
    )