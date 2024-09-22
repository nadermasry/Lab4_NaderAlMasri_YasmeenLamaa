# models.py
class Person:
    """
    A class representing a person with basic attributes like name, age, and email.

    Attributes:
        name (str): The name of the person.
        age (int): The age of the person.
        _email (str): The private email address of the person.
    """
    def __init__(self, name, age, email):
        """
        Initialize the Person object with a name, age, and email.

        Parameters:
            name (str): The name of the person.
            age (int): The age of the person.
            email (str): The email address of the person.
        """
        self.name = name
        self.age = age
        self._email = email

    def introduce(self):
        """
        Introduce the person.

        Returns:
            str: A string introducing the person with their name and age.
        """
        return f"Hello, my name is {self.name} and I am {self.age} years old."

class Student(Person):
    """
    A class representing a student, which inherits from the Person class.

    Attributes:
        student_id (str): The unique ID of the student.
        registered_courses (list): A list of courses the student has registered for.
    """
    def __init__(self, name, age, email, student_id):
        """
        Initialize the Student object with a name, age, email, and student ID.

        Parameters:
            name (str): The name of the student.
            age (int): The age of the student.
            email (str): The email address of the student.
            student_id (str): The unique ID of the student.
        """
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """
        Register the student for a course.

        Parameters:
            course (Course): The course to register the student for.

        Actions:
            - Adds the course to the student's list of registered courses.
        """
        self.registered_courses.append(course)

class Instructor(Person):
    """
    A class representing an instructor, which inherits from the Person class.

    Attributes:
        instructor_id (str): The unique ID of the instructor.
        assigned_courses (list): A list of courses assigned to the instructor.
    """
    def __init__(self, name, age, email, instructor_id):
        """
        Initialize the Instructor object with a name, age, email, and instructor ID.

        Parameters:
            name (str): The name of the instructor.
            age (int): The age of the instructor.
            email (str): The email address of the instructor.
            instructor_id (str): The unique ID of the instructor.
        """
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """
        Assign the instructor to a course.

        Parameters:
            course (Course): The course to assign to the instructor.

        Actions:
            - Adds the course to the instructor's list of assigned courses.
        """
        self.assigned_courses.append(course)

class Course:
    """
    A class representing a course.

    Attributes:
        course_id (str): The unique ID of the course.
        course_name (str): The name of the course.
        instructor (Instructor): The instructor assigned to the course.
        students (list): A list of students enrolled in the course.
    """
    def __init__(self, course_id, course_name, instructor):
        """
        Initialize the Course object with a course ID, course name, and instructor.

        Parameters:
            course_id (str): The unique ID of the course.
            course_name (str): The name of the course.
            instructor (Instructor): The instructor assigned to the course.
        """
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.students = []  

    def add_student(self, student):
        """
        Add a student to the course.

        Parameters:
            student (Student): The student to be added to the course.

        Actions:
            - Adds the student to the course's list of students.
        """
        self.students.append(student)