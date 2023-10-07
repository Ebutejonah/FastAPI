from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "John",
        "age": 17,
        "year": "grade 12",
   }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name : Optional[str] = None
    age : Optional[int] = None
    year : Optional[str] = None

@app.get("/")
def index():
    return {"name":"First Data"}


@app.get("/get-student/{student_id}")
def get_student(student_id: int= Path(description="The ID of the student of interest")):
    return students[student_id]


@app.get("/get-student-by-name")
def get_student(name : Optional[str] = None):
    for student in students:
        if name == students[student]["name"]:
            return students[student]
        return{"Data": "Not Found"}
    

@app.post("/create-student/{student_id}")
def create_student(student_id : int, student : Student):
    if student_id in students:
        return{"Data" : "Already Exists"}
    students[student_id] = student
    return students[student_id]


@app.put("/update-student/{student_id}")
def update_student(student_id : int, student : UpdateStudent):
    if student_id in students:
        if student.name != None:
            students[student_id]["name"] = student.name
        if student.age != None:
            students[student_id]["age"] = student.age
        if student.year != None:
            students[student_id]["year"] = student.year
        return students[student_id]
    return {"Data" : "No Student with ID exists"}