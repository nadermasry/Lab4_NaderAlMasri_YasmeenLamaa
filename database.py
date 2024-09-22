#database.py
import sqlite3

def create_database():
    """
    Create the database and necessary tables for the School Management System.

    This function creates four tables:
    - Students: Stores student information (student_id, name, age, email).
    - Instructors: Stores instructor information (instructor_id, name, age, email).
    - Courses: Stores course information (course_id, course_name, instructor_id), and establishes
      a foreign key relationship with the Instructors table.
    - Registrations: Links students to courses, with foreign keys referencing both the Students and Courses tables.

    If the tables already exist, they will not be recreated.
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Create Students table
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL
    )''')

    # Create Instructors table
    cursor.execute('''CREATE TABLE IF NOT EXISTS instructors (
        instructor_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL
    )''')

    # Create Courses table
    cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
        course_id TEXT PRIMARY KEY,
        course_name TEXT NOT NULL,
        instructor_id TEXT NOT NULL,
        FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
    )''')

    # Create Registrations table
    cursor.execute('''CREATE TABLE IF NOT EXISTS registrations (
        student_id TEXT,
        course_id TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (course_id) REFERENCES courses(course_id),
        PRIMARY KEY (student_id, course_id)
    )''')

    conn.commit()
    conn.close()
def db_add_student(student_id, name, age, email):
    """
    Add a new student to the Students table.

    Parameters:
        student_id (str): The unique identifier for the student.
        name (str): The name of the student.
        age (int): The age of the student.
        email (str): The email of the student.
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (student_id, name, age, email) VALUES (?, ?, ?, ?)', 
                   (student_id, name, age, email))
    conn.commit()
    conn.close()

def db_add_instructor(instructor_id, name, age, email):
    """
    Add a new instructor to the Instructors table.

    Parameters:
        instructor_id (str): The unique identifier for the instructor.
        name (str): The name of the instructor.
        age (int): The age of the instructor.
        email (str): The email of the instructor.
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)', 
                   (instructor_id, name, age, email))
    conn.commit()
    conn.close()

def db_add_course(course_id, course_name, instructor_id):
    """
    Add a new course to the Courses table.

    Parameters:
        course_id (str): The unique identifier for the course.
        course_name (str): The name of the course.
        instructor_id (str): The ID of the instructor assigned to the course (must exist in the Instructors table).
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    if not instructor_id:
        instructor_id=""
    cursor.execute('INSERT INTO courses (course_id, course_name, instructor_id) VALUES (?, ?, ?)', 
                   (course_id, course_name, instructor_id))
    conn.commit()
    conn.close()

def fetch_students():
    """
    Fetch all students from the Students table.

    Returns:
        list of tuple: A list of all students, where each student is represented as a tuple 
        (student_id, name, age, email).
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return students

def fetch_instructors():
    """
    Fetch all instructors from the Instructors table.

    Returns:
        list of tuple: A list of all instructors, where each instructor is represented as a tuple 
        (instructor_id, name, age, email).
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM instructors')
    instructors = cursor.fetchall()
    conn.close()
    return instructors

def fetch_courses():
    """
    Fetch all courses from the Courses table.

    Returns:
        list of tuple: A list of all courses, where each course is represented as a tuple 
        (course_id, course_name, instructor_id).
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()
    conn.close()
    return courses

def db_update_student(student_id, name, age, email):
    """
    Update the details of an existing student in the Students table.

    Parameters:
        student_id (str): The unique identifier of the student to update.
        name (str): The updated name of the student.
        age (int): The updated age of the student.
        email (str): The updated email of the student.
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    try:
        # Print statement to verify parameters
        print(f"Updating student: {student_id}, {name}, {age}, {email}")

        # Update student details in the database
        cursor.execute('''
            UPDATE students 
            SET name = ?, age = ?, email = ?
            WHERE student_id = ?
        ''', (name, age, email, student_id))

        # Ensure that changes are committed to the database
        conn.commit()

        # Check if the update was successful
        if cursor.rowcount == 0:
            print(f"No student found with ID: {student_id}")
        else:
            print(f"Student {student_id} updated successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()


def db_update_instructor(instructor_id, name, age, email):
    """
    Update the details of an existing instructor in the Instructors table.

    Parameters:
        instructor_id (str): The unique identifier of the instructor to update.
        name (str): The updated name of the instructor.
        age (int): The updated age of the instructor.
        email (str): The updated email of the instructor.

    Actions:
        - Updates the instructor's name, age, and email in the database for the specified instructor ID.
        - Commits the changes to the database after the update.
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE instructors SET name = ?, age = ?, email = ? WHERE instructor_id = ?', 
                   (name, age, email, instructor_id))
    conn.commit()
    conn.close()

def db_update_course(course_id, course_name, instructor_id):
    """
    Update the details of an existing course in the Courses table.

    Parameters:
        course_id (str): The unique identifier of the course to update.
        course_name (str): The updated name of the course.
        instructor_id (str): The ID of the instructor assigned to the course.

    Actions:
        - Updates the course name and instructor ID for the specified course.
        - Commits the changes to the database after the update.
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE courses SET course_name = ?, instructor_id = ? WHERE course_id = ?', 
                   (course_name, instructor_id, course_id))
    conn.commit()
    conn.close()
def delete_student(student_id):
    """
    Delete a student from the Students table.

    Parameters:
        student_id (str): The unique identifier of the student to delete.

    Actions:
        - Deletes the student from the database based on the student ID.
        - Commits the deletion to the database.
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()

def delete_instructor(instructor_id):
    """
    Delete an instructor from the Instructors table.

    Parameters:
        instructor_id (str): The unique identifier of the instructor to delete.

    Actions:
        - Deletes the instructor from the database based on the instructor ID.
        - Commits the deletion to the database.
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM instructors WHERE instructor_id = ?', (instructor_id,))
    conn.commit()
    conn.close()

def delete_course(course_id):
    """
    Delete a course from the Courses table.

    Parameters:
        course_id (str): The unique identifier of the course to delete.

    Actions:
        - Deletes the course from the database based on the course ID.
        - Commits the deletion to the database.
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM courses WHERE course_id = ?', (course_id,))
    conn.commit()
    conn.close()

def fetch_registered_students(course_id):
    """
    Fetch all students registered for a specific course by course ID.

    Parameters:
        course_id (str): The unique identifier of the course.

    Returns:
        list of tuple: A list of students registered for the course, where each student is represented 
        as a tuple (student_id, name, email, age).

    Actions:
        - Queries the database to retrieve all students who are registered for the specified course.
        - Joins the Students and Registrations tables to obtain the details of registered students.
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    
    query = '''
    SELECT students.student_id, students.name, students.email, students.age 
    FROM students
    JOIN registrations ON students.student_id = registrations.student_id
    WHERE registrations.course_id = ?
    '''
    
    cursor.execute(query, (course_id,))
    registered_students = cursor.fetchall()
    conn.close()
    
    return registered_students

def db_register_student_to_course(student_name, course_id):
    """
    Registers a student to a course in the database.

    This function fetches the student ID for the given `student_name` by searching 
    through the students table. If the student is found, it inserts a new record 
    into the `registrations` table to register the student for the specified course.

    :param student_name: The name of the student to be registered.
    :param course_id: The ID of the course the student is being registered for.

    :raises sqlite3.Error: If the database insertion fails, the transaction is rolled back.

    :return: None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    
    student_id = None
    students = fetch_students()
    for student in students:
        if student[1] == student_name:
            student_id = student[0]
            break
    
    if student_id:
        try:
            cursor.execute('INSERT INTO registrations (student_id, course_id) VALUES (?, ?)', (student_id, course_id))
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
        finally:
            conn.close()
    else:
        print("Error", f"Student {student_name} not found")

# Function to assign an instructor to a course
def db_assign_course_to_instructor(instructor_name, course_id):
    """
    Assigns an instructor to a course in the database.

    This function fetches the instructor ID for the given `instructor_name` by searching 
    through the instructors table. If the instructor is found, it updates the `courses` 
    table to assign the instructor to the specified course.

    :param instructor_name: The name of the instructor to assign.
    :param course_id: The ID of the course the instructor is being assigned to.

    :raises sqlite3.Error: If the database update fails, the transaction is rolled back.

    :return: None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    instructor_id = None
    instructors = fetch_instructors()
    for instructor in instructors:
        if instructor[1] == instructor_name:
            instructor_id = instructor[0]
            break
    
    if instructor_id:
        try:
            cursor.execute('UPDATE courses SET instructor_id = ? WHERE course_id = ?', (instructor_id, course_id))
            conn.commit()
            print("Success", f"{instructor_name} has been assigned to {course_id}")
        except sqlite3.Error as e:
            conn.rollback()
            print("Error", str(e))
        finally:
            conn.close()
    else:
        print("Error", f"Instructor {instructor_name} not found")
