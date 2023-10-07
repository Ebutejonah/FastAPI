class Human:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        return self.age
    
    def get_details(self):
        return f"{self.get_full_name()} is {self.age} years old"
    

class Student(Human):
    def __init__(self, first_name, last_name, age, grade, school):
        super().__init__(first_name, last_name, age)
        self.grade = grade
        self.school = school

    def get_grade(self):
        return self.grade
    
    def get_details(self):
        return f"{self.get_full_name()} is {self.age} years old and has a grade of {self.get_grade()}. He is also a student of {self.school}"

student1 = Student("Jonah", "Ebute", 28, 1, "Altschool Africa")
print(student1.get_details())
#print(student1.get_grade())