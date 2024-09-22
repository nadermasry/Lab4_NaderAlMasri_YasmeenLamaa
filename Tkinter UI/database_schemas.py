import sqlite3

def create_database():
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Students table
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL
    )''')

    # Instructors table
    cursor.execute('''CREATE TABLE IF NOT EXISTS instructors (
        instructor_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL
    )''')

    # Courses table
    cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
        course_id TEXT PRIMARY KEY,
        course_name TEXT NOT NULL,
        instructor_id TEXT NOT NULL,
        FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
    )''')

    # Registrations table
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
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (student_id, name, age, email) VALUES (?, ?, ?, ?)', 
                   (student_id, name, age, email))
    conn.commit()
    conn.close()

def db_add_instructor(instructor_id, name, age, email):
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)', 
                   (instructor_id, name, age, email))
    conn.commit()
    conn.close()

def db_add_course(course_id, course_name, instructor_id):
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    if not instructor_id:
        instructor_id=""
    cursor.execute('INSERT INTO courses (course_id, course_name, instructor_id) VALUES (?, ?, ?)', 
                   (course_id, course_name, instructor_id))
    conn.commit()
    conn.close()

def fetch_students():
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return students

def fetch_instructors():
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM instructors')
    instructors = cursor.fetchall()
    conn.close()
    return instructors

def fetch_courses():
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()
    conn.close()
    return courses

def db_update_student(student_id, name, age, email):
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

    
        conn.commit()

        if cursor.rowcount == 0:
            print(f"No student found with ID: {student_id}")
        else:
            print(f"Student {student_id} updated successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()


def db_update_instructor(instructor_id, name, age, email):
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE instructors SET name = ?, age = ?, email = ? WHERE instructor_id = ?', 
                   (name, age, email, instructor_id))
    conn.commit()
    conn.close()

def db_update_course(course_id, course_name):
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE courses SET course_name = ? WHERE course_id = ?', 
                   (course_name, course_id))
    conn.commit()
    conn.close()
def delete_student(student_id):
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()

def delete_instructor(instructor_id):
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM instructors WHERE instructor_id = ?', (instructor_id,))
    conn.commit()
    conn.close()

def delete_course(course_id):
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM courses WHERE course_id = ?', (course_id,))
    conn.commit()
    conn.close()

def fetch_registered_students(course_id):
    """Fetch all students registered for a specific course by course_id."""
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
