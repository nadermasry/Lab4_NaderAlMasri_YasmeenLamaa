import json
from data_validation import validate_age,validate_course_id,validate_course_name,validate_email,validate_instructor_id,validate_name,validate_student_id

# Person Class
class Person:
    def __init__(self, name: str, age: int, email: str):
        validate_name(name)
        validate_age(int(age))
        validate_email(email)
        self.name = name
        self.age = age
        self.__email = email  

    def introduce(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    #for serialization 
    def change_to_dictionary(self):
        return {'name': self.name, 'age': self.age, 'email': self.__email}

    def get_email(self):
        return self.__email
    
# Student Subclass
class Student(Person):
    def __init__(self, name: str, age: int, email: str, student_id: str, registered_courses: list):
        super().__init__(name, age, email)
        validate_student_id(str(student_id))
        self.student_id = student_id
        self.registered_courses = registered_courses

    def register_course(self, course):
        #part of data validation
        if isinstance(course, Course):
            self.registered_courses.append(course)
        else:
            raise ValueError("Course must be an instance of Course.")

    #for serialization 
    def change_to_dictionary(self):
        data = super().change_to_dictionary()
        data.update({
            'student_id': self.student_id,
            'registered_courses': self.registered_courses
        })
        return data

# Instructor Subclass 
class Instructor(Person):
    def __init__(self, name: str, age: int, email: str, instructor_id: str, assigned_courses: list):
        super().__init__(name, age, email)
        validate_instructor_id(instructor_id)
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses  

    def assign_course(self, course):
        #part of data validation 
        if isinstance(course, Course):
            self.assigned_courses.append(course)
        else:
            raise ValueError("Assigned course must be an instance of Course.")

    #for serialization
    def change_to_dictionary(self):
        data = super().change_to_dictionary()
        data.update({
            'instructor_id': self.instructor_id,
            'assigned_courses': self.assigned_courses
        })
        return data
    

    
# Course Class
class Course:
    def __init__(self, course_id: str, course_name: str, instructor: Instructor , enrolled_students: list):
        validate_course_id(course_id)
        validate_course_name(course_name)
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = enrolled_students

    def add_student(self, student: Student):
        #part of data validation 
        if isinstance(student, Student):
            self.enrolled_students.append(student)
        else:
            raise ValueError("Enrolled student must be an instance of Student.")
    
    #for serialization
    def change_to_dictionary(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor': self.instructor.change_to_dictionary(),
            'enrolled_students': [student.change_to_dictionary() for student in self.enrolled_students]
        }
    

#serialize
def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

#deserialize 
def load_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)