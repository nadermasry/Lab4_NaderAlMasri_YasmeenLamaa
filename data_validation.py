import re

def validate_name(name):
    if not name or len(name.strip()) <= 1:
        raise ValueError("Name must be more than one character.")
    return name

def validate_age(age):
    if age < 0:
        raise ValueError("Age must be non-negative.")
    return age

def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise ValueError("Invalid email format.")
    return email

def validate_student_id(student_id:str):
    if not student_id or not student_id.strip():
        raise ValueError("Student ID cannot be empty.")
    return student_id


def validate_instructor_id(instructor_id: str):
    if not instructor_id or not instructor_id.strip():
        raise ValueError("Instructor ID cannot be empty.")
    return instructor_id


def validate_course_id(course_id: str):
    if not course_id or not course_id.strip():
        raise ValueError("Course ID cannot be empty.")
    return course_id

def validate_course_name(course_name:str):
    if not course_name or not course_name.strip():
        raise ValueError("Course name cannot be empty.")
    return course_name

