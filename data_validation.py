import re

def validate_name(name):
    """
    Validates the provided name to ensure it is not empty and has more than one character.

    :param name: The name to validate (string).
    
    :raises ValueError: If the name is empty or less than two characters after trimming.
    
    :return: The validated name.
    """
    if not name or len(name.strip()) <= 1:
        raise ValueError("Name must be more than one character.")
    return name

def validate_age(age):
    """
    Validates that the provided age is non-negative.

    :param age: The age to validate (integer).
    
    :raises ValueError: If the age is negative.
    
    :return: The validated age.
    """
    if age < 0:
        raise ValueError("Age must be non-negative.")
    return age

def validate_email(email):
    """
    Validates that the provided email is in a valid format.

    :param email: The email to validate (string).
    
    :raises ValueError: If the email does not match the standard email format.
    
    :return: The validated email.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise ValueError("Invalid email format.")
    return email

def validate_student_id(student_id:str):
    """
    Validates that the provided student ID is not empty or blank.

    :param student_id: The student ID to validate (string).
    
    :raises ValueError: If the student ID is empty or blank.
    
    :return: The validated student ID.
    """
    if not student_id or not student_id.strip():
        raise ValueError("Student ID cannot be empty.")
    return student_id


def validate_instructor_id(instructor_id: str):
    """
    Validates that the provided instructor ID is not empty or blank.

    :param instructor_id: The instructor ID to validate (string).
    
    :raises ValueError: If the instructor ID is empty or blank.
    
    :return: The validated instructor ID.
    """
    if not instructor_id or not instructor_id.strip():
        raise ValueError("Instructor ID cannot be empty.")
    return instructor_id


def validate_course_id(course_id: str):
    """
    Validates that the provided course ID is not empty or blank.

    :param course_id: The course ID to validate (string).
    
    :raises ValueError: If the course ID is empty or blank.
    
    :return: The validated course ID.
    """
    if not course_id or not course_id.strip():
        raise ValueError("Course ID cannot be empty.")
    return course_id

def validate_course_name(course_name:str):
    """
    Validates that the provided course name is not empty or blank.

    :param course_name: The course name to validate (string).
    
    :raises ValueError: If the course name is empty or blank.
    
    :return: The validated course name.
    """
    if not course_name or not course_name.strip():
        raise ValueError("Course name cannot be empty.")
    return course_name

