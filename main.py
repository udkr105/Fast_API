from fastapi import FastAPI


app=FastAPI()

# Define GET API

@app.get("/")

def home():

    return {"message": "Welcome to FastAPI"}



# Define GET API with /student Endpoint

@app.get("/student")

def get_student():

    return{

        "id":101,

        "name":"Allen",

        "course":"Python Fast API"

    }


@app.get("/students/{student_id}")

def get_student(student_id: int):

    return {"student_id": student_id}









