from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# --------------------------------
# 1. Python Data Structure (Mock DB)
# --------------------------------
students = [
    {
        "id": 1,
        "name": "Rahul",
        "age": 25,
        "course": "Java",
        "city": "Pune"
    },
    {
        "id": 2,
        "name": "Amit",
        "age": 28,
        "course": "Python",
        "city": "Mumbai"
    },
    {
        "id": 3,
        "name": "Priya",
        "age": 24,
        "course": "Java",
        "city": "Hyd"
    }
]

# --------------------------------
# 2. Pydantic Model
# --------------------------------
class Student(BaseModel):
    name: str
    age: int
    course: str
    city: str

# --------------------------------
# 3. CREATE - POST
# --------------------------------
@app.post("/students")
def create_student(student: Student):
    new_student = {
        "id": max([s["id"] for s in students], default=0) + 1,
        "name": student.name,
        "age": student.age,
        "course": student.course,
        "city": student.city
    }
    students.append(new_student)
    return {
        "message": "Student created successfully",
        "data": new_student
    }

# --------------------------------
# 4. READ ALL & FILTER - GET
# --------------------------------
@app.get("/students")
def get_students(course: Optional[str] = None, city: Optional[str] = None):
    result = students

    if course:
        result = [
            s for s in result
            if s["course"].lower() == course.lower()
        ]

    if city:
        result = [
            s for s in result
            if s["city"].lower() == city.lower()
        ]

    return {
        "total": len(result),
        "data": result
    }

# --------------------------------
# 5. READ ONE BY ID - GET
# --------------------------------
@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return {"data": student}
    raise HTTPException(status_code=404, detail="Student not found")