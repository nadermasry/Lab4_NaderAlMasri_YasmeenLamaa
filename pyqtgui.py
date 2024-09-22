import sys
import json
import csv
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, \
    QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, QComboBox, QMessageBox, QHeaderView, QDialog, QFileDialog
from PyQt5.QtCore import Qt
from database import create_database, db_add_student, db_add_instructor, db_add_course, fetch_students, fetch_instructors, fetch_courses, \
    db_update_student, db_update_instructor, db_update_course, delete_student, delete_instructor, delete_course, fetch_registered_students
from models import Student, Instructor, Course

"""
School Management System Application using PyQt5.

This module defines a school management system where users can manage students, instructors, and courses.
The application provides a graphical user interface (GUI) to perform CRUD (Create, Read, Update, Delete)
operations on students, instructors, and courses. Users can register students to courses, search records,
export data to CSV files, and save or load the data from JSON files.

Classes:
    SchoolManagementSystemApp(QMainWindow): Main window of the school management system. Provides functionality
    for managing students, instructors, and courses, as well as registering students in courses.
"""

class SchoolManagementSystemApp(QMainWindow):
    """
    Main window for the School Management System Application using PyQt5.

    This class provides the main functionality for managing students, instructors, courses, and student registrations.
    Users can add, edit, delete, search, and display students, instructors, and courses. Additionally, the class
    supports saving and loading data from JSON files, exporting to CSV, and viewing registered students per course.

    Attributes:
        students (list): List of students currently loaded from the database.
        instructors (list): List of instructors currently loaded from the database.
        courses (list): List of courses currently loaded from the database.
    """
    def __init__(self):
        """
        Initialize the SchoolManagementSystemApp window and its attributes.

        Calls the setup_ui function to set up the user interface, and load_data function to load students,
        instructors, and courses from the database. 
        """
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Initialize database
        create_database()
        self.students = []  # Add this line
        self.instructors = []  # Add this line
        self.courses = []  # Add this line


        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """
        Set up the user interface with tabs for managing students, instructors, courses, and registrations.

        Initializes the main layout and adds the following tabs:
        - Students: Allows users to add, edit, delete, and display student records.
        - Instructors: Allows users to add, edit, delete, and display instructor records.
        - Courses: Allows users to add, edit, delete, and display course records.
        - Student Registration: Allows users to register students to courses.
        """
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        header = QLabel("School Management System")
        header.setStyleSheet("font: bold 16px; background-color: #4CAF50; color: white; padding: 10px;")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.student_tab = QWidget()
        self.instructor_tab = QWidget()
        self.course_tab = QWidget()
        self.registration_tab = QWidget()

        self.tab_widget.addTab(self.student_tab, "Students")
        self.tab_widget.addTab(self.instructor_tab, "Instructors")
        self.tab_widget.addTab(self.course_tab, "Courses")
        self.tab_widget.addTab(self.registration_tab, "Student Registration")

        self.setup_student_form()
        self.setup_instructor_form()
        self.setup_course_form()
        self.setup_registration_form()
        self.setup_display_records(main_layout)
        self.setup_switch_buttons(main_layout)

        self.setup_data_buttons(main_layout)
        self.setup_search(main_layout)


    def setup_display_records(self, layout):
        """
        Set up the main table to display records of students, instructors, and courses.

        This method creates a QTableWidget to display records, which will be populated by
        the load_data method with student, instructor, and course data.

        Parameters:
            layout (QVBoxLayout): The main layout of the application where the table is added.
        """
        table_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)  # ID, Name, Email, Age, Type
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Age", "Type"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        table_layout.addWidget(self.table)
        layout.addLayout(table_layout)


    def setup_switch_buttons(self, layout):
        """
        Set up buttons to switch between views of registered students, instructors, and courses.

        Adds buttons for:
        - Viewing registered students for a specific course.
        - Viewing all instructors.
        - Viewing all courses.

        Parameters:
            layout (QVBoxLayout): The main layout where the buttons are added.
        """
        switch_layout = QHBoxLayout()
        
        self.switch_button = QPushButton("Show Registered Students")
        self.switch_button.clicked.connect(self.select_course_to_view)
        switch_layout.addWidget(self.switch_button)
        
        self.show_instructors_button = QPushButton("Show Instructors")
        self.show_instructors_button.clicked.connect(self.show_instructors)
        switch_layout.addWidget(self.show_instructors_button)
        
        self.show_courses_button = QPushButton("Show Courses")
        self.show_courses_button.clicked.connect(self.show_courses)
        switch_layout.addWidget(self.show_courses_button)

        layout.addLayout(switch_layout)

    def setup_data_buttons(self, layout):
        """
        Set up buttons for saving, refreshing, editing, and deleting data records.

        Adds buttons to:
        - Save data to a JSON file.
        - Refresh the table with the latest data.
        - Edit a selected record.
        - Delete a selected record.

        Parameters:
            layout (QVBoxLayout): The main layout where the buttons are added.
        """
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Save Data")
        self.save_button.clicked.connect(self.save_data)
        button_layout.addWidget(self.save_button)

        self.refresh_button = QPushButton("Refresh Data")
        self.refresh_button.clicked.connect(self.load_data)
        button_layout.addWidget(self.refresh_button)

        self.edit_button = QPushButton("Edit Record")
        self.edit_button.clicked.connect(self.edit_record)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Record")
        self.delete_button.clicked.connect(self.delete_record)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)


    def export_to_csv(self):
        """
    Export the current students, instructors, and courses data to a CSV file.

    The user is prompted to choose a location and filename to save the CSV file.
    The data is exported in three sections: Students, Instructors, and Courses, each with its own
    set of column headers and data rows.

    - Students: Includes student ID, name, email, and age.
    - Instructors: Includes instructor ID, name, email, and age.
    - Courses: Includes course ID, course name, instructor name, and a list of registered student IDs.

    If the export is successful, a message box is displayed to confirm the export.

    Raises:
        None
    """
        # Prompt the user to choose a location and filename for the CSV file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)", options=options)
        
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)

                # Export Students
                writer.writerow(["Students"])  # Section header
                writer.writerow(["Student ID", "Name", "Email", "Age"])  # Column headers
                for student in self.students:
                    writer.writerow([student.student_id, student.name, student._email, student.age])

                writer.writerow([])  # Empty row for separation

                # Export Instructors
                writer.writerow(["Instructors"])  # Section header
                writer.writerow(["Instructor ID", "Name", "Email", "Age"])  # Column headers
                for instructor in self.instructors:
                    writer.writerow([instructor.instructor_id, instructor.name, instructor._email, instructor.age])

                writer.writerow([])  # Empty row for separation

                # Export Courses
                writer.writerow(["Courses"])  # Section header
                writer.writerow(["Course ID", "Course Name", "Instructor Name", "Registered Students (IDs)"])  # Column headers
                for course in self.courses:
                    student_ids = ", ".join([student.student_id for student in course.students])  # List student IDs
                    writer.writerow([course.course_id, course.course_name, course.instructor.name, student_ids])

            QMessageBox.information(self, "Export Successful", f"Data successfully exported to {file_path}")

    def show_instructors(self):
        """
    Display a new window with a list of all instructors in the system.

    The window includes a table displaying instructor details such as:
    - ID
    - Name
    - Email
    - Age

    A search feature is also provided to filter instructors based on the search query.

    Raises:
        None
    """
        instructor_window = QMainWindow(self)
        instructor_window.setWindowTitle("Instructors List")
        instructor_window.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()
        central_widget = QWidget()
        instructor_window.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Age"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Assuming instructors is a list of tuples (instructor_id, name, email, age)
        for instructor in self.instructors:
            row_position = table.rowCount()
            table.insertRow(row_position)

            # Access tuple elements by index
            table.setItem(row_position, 0, QTableWidgetItem(str(instructor[0])))  # instructor_id
            table.setItem(row_position, 1, QTableWidgetItem(instructor[1]))       # name
            table.setItem(row_position, 2, QTableWidgetItem(instructor[2]))       # email
            table.setItem(row_position, 3, QTableWidgetItem(str(instructor[3])))  # age

        layout.addWidget(table)

        search_layout = QHBoxLayout()
        search_label = QLabel("Search Instructors")
        search_entry = QLineEdit()
        search_button = QPushButton("Search")
        search_button.clicked.connect(lambda: self.search_instructors(table, search_entry.text()))
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_entry)
        search_layout.addWidget(search_button)

        layout.addLayout(search_layout)

        instructor_window.show()


    def show_courses(self):
        """
    Display a new window with a list of all courses in the system.

    The window includes a table displaying course details such as:
    - Course ID
    - Course Name
    - Instructor Name

    A search feature is provided to filter courses based on the search query.

    Raises:
        None
    """
        courses_popup = QDialog(self)
        courses_popup.setWindowTitle("Courses List")
        courses_popup.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        search_label = QLabel("Search Courses")
        search_entry = QLineEdit()
        search_button = QPushButton("Search")
        search_button.clicked.connect(lambda: self.search_courses(treeview, search_entry.text()))
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_entry)
        search_layout.addWidget(search_button)

        layout.addLayout(search_layout)

        treeview = QTableWidget()
        treeview.setColumnCount(3)
        treeview.setHorizontalHeaderLabels(["Course ID", "Course Name", "Instructor"])
        treeview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for course in self.courses:
            row_position = treeview.rowCount()
            treeview.insertRow(row_position)
            treeview.setItem(row_position, 0, QTableWidgetItem(str(course[0])))  # course_id
            treeview.setItem(row_position, 1, QTableWidgetItem(course[1]))       # course_name
            treeview.setItem(row_position, 2, QTableWidgetItem(course[2]))       # instructor_name
        layout.addWidget(treeview)
        courses_popup.setLayout(layout)
        courses_popup.exec_()


    def select_course_to_view(self):
        """
    Display a popup window for the user to select a course and view registered students.

    Once a course is selected, the list of registered students for that course will be displayed.

    Raises:
        None
    """
        self.popup = QDialog(self)
        self.popup.setWindowTitle("Select Course")
        self.popup.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        label = QLabel("Select Course")
        self.view_course_combo = QComboBox()

        # Add courses to the combo box, make sure self.courses is populated
        if not self.courses:
            QMessageBox.critical(self, "Error", "No courses available.")
        else:
            self.view_course_combo.addItems([course[1] for course in self.courses])  # Access course_name via tuple index

        show_students_button = QPushButton("Show Students")
        show_students_button.clicked.connect(self.show_registered_students)

        layout.addWidget(label)
        layout.addWidget(self.view_course_combo)
        layout.addWidget(show_students_button)

        self.popup.setLayout(layout)
        self.popup.exec_()

    def setup_student_form(self):
        """
    Set up the form for adding and managing student records.

    This form contains input fields for:
    - Student Name
    - Student Age
    - Student Email
    - Student ID

    It also includes a button to add the student to the database.
    """
        layout = QVBoxLayout(self.student_tab)

        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()
        self.student_id = QLineEdit()

        layout.addWidget(QLabel("Name"))
        layout.addWidget(self.student_name)
        layout.addWidget(QLabel("Age"))
        layout.addWidget(self.student_age)
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.student_email)
        layout.addWidget(QLabel("Student ID"))
        layout.addWidget(self.student_id)

        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.clicked.connect(self.add_student)
        layout.addWidget(self.add_student_button)

    def setup_instructor_form(self):
        """
    Set up the form for adding and managing instructor records.

    This form contains input fields for:
    - Instructor Name
    - Instructor Age
    - Instructor Email
    - Instructor ID

    It also includes a button to add the instructor to the database.
    """
        layout = QVBoxLayout(self.instructor_tab)

        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()
        self.instructor_id = QLineEdit()

        layout.addWidget(QLabel("Name"))
        layout.addWidget(self.instructor_name)
        layout.addWidget(QLabel("Age"))
        layout.addWidget(self.instructor_age)
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.instructor_email)
        layout.addWidget(QLabel("Instructor ID"))
        layout.addWidget(self.instructor_id)

        self.add_instructor_button = QPushButton("Add Instructor")
        self.add_instructor_button.clicked.connect(self.add_instructor)
        layout.addWidget(self.add_instructor_button)

    def setup_course_form(self):
        """
    Set up the form for adding and managing course records.

    This form contains input fields for:
    - Course Name
    - Course ID
    - Instructor (Dropdown for selecting an instructor)

    It also includes a button to add the course to the database.
    """
        layout = QVBoxLayout(self.course_tab)

        self.course_name = QLineEdit()
        self.course_id = QLineEdit()
        self.course_instructor = QComboBox()

        layout.addWidget(QLabel("Course Name"))
        layout.addWidget(self.course_name)
        layout.addWidget(QLabel("Course ID"))
        layout.addWidget(self.course_id)
        layout.addWidget(QLabel("Instructor"))
        layout.addWidget(self.course_instructor)

        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.clicked.connect(self.add_course)
        layout.addWidget(self.add_course_button)

    def setup_registration_form(self):
        """
    Set up the form for registering students to courses.

    This form contains dropdowns for selecting:
    - A student from a list of registered students
    - A course from a list of available courses

    It also includes a button to register the selected student for the selected course.
    """
        layout = QVBoxLayout(self.registration_tab)

        self.registration_student = QComboBox()
        self.registration_course = QComboBox()

        layout.addWidget(QLabel("Select Student"))
        layout.addWidget(self.registration_student)
        layout.addWidget(QLabel("Select Course"))
        layout.addWidget(self.registration_course)

        self.register_button = QPushButton("Register Student")
        self.register_button.clicked.connect(self.register_student)
        layout.addWidget(self.register_button)

    def search_instructors(self, table_widget, search_query):
        """
    Search for instructors in the system based on a search query.

    Filters the list of instructors by checking if the search query matches the instructor's ID or name.
    Updates the provided table widget with the filtered results.

    Parameters:
        table_widget (QTableWidget): The table to display the filtered instructors.
        search_query (str): The query used to search for instructors by name or ID.
    """
        table_widget.setRowCount(0)  # Clear the table

        for instructor in self.instructors:
            if search_query.lower() in instructor[1].lower() or search_query.lower() in instructor[0].lower():
                row_position = table_widget.rowCount()
                table_widget.insertRow(row_position)
                table_widget.setItem(row_position, 0, QTableWidgetItem(instructor[0]))  # instructor_id
                table_widget.setItem(row_position, 1, QTableWidgetItem(instructor[1]))  # name
                table_widget.setItem(row_position, 2, QTableWidgetItem(instructor[2]))  # email
                table_widget.setItem(row_position, 3, QTableWidgetItem(str(instructor[3])))  # age

    def search_courses(self, table_widget, search_query):
        """
    Search for courses in the system based on a search query.

    Filters the list of courses by checking if the search query matches the course's ID or name.
    Updates the provided table widget with the filtered results.

    Parameters:
        table_widget (QTableWidget): The table to display the filtered courses.
        search_query (str): The query used to search for courses by name or ID.
    """
        table_widget.setRowCount(0)  # Clear the table

        for course in self.courses:
            # Access the tuple elements by index
            if search_query.lower() in course[1].lower() or search_query.lower() in course[0].lower():
                row_position = table_widget.rowCount()
                table_widget.insertRow(row_position)
                table_widget.setItem(row_position, 0, QTableWidgetItem(course[0]))  # course_id
                table_widget.setItem(row_position, 1, QTableWidgetItem(course[1]))  # course_name
                table_widget.setItem(row_position, 2, QTableWidgetItem(course[2]))  # instructor name

    def show_registered_students(self):
        """
    Display a new window with the list of students registered for the selected course.

    After selecting a course from the dropdown, this method fetches the students registered for that course
    and displays them in a popup window. If no students are registered for the course, an information message is shown.

    Raises:
        None
    """
        course_name = self.view_course_combo.currentText()  # Get selected course name
        course = next((c for c in self.courses if c[1] == course_name), None)  # Access tuple by index

        if course is None:
            QMessageBox.critical(self, "Error", "Please select a valid course.")
            return

        # Assuming 'course' is a tuple (course_id, course_name, instructor_id)
        course_id = course[0]  # Extract the course_id from the tuple

        # Fetch the registered students using the course ID
        registered_students = fetch_registered_students(course_id)

        if not registered_students:
            QMessageBox.information(self, "Info", f"No students registered for {course_name}.")
            return

        # Create a popup to display the students
        student_popup = QDialog(self)
        student_popup.setWindowTitle(f"Students Registered for {course_name}")
        student_popup.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        treeview = QTableWidget()
        treeview.setColumnCount(4)
        treeview.setHorizontalHeaderLabels(["ID", "Name", "Email", "Age"])
        treeview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Iterate through the registered_students list (which should be tuples)
        for student in registered_students:
            row_position = treeview.rowCount()
            treeview.insertRow(row_position)

            # Assuming student is a tuple (student_id, name, email, age)
            treeview.setItem(row_position, 0, QTableWidgetItem(str(student[0])))  # student_id
            treeview.setItem(row_position, 1, QTableWidgetItem(student[1]))        # name
            treeview.setItem(row_position, 2, QTableWidgetItem(student[2]))        # email
            treeview.setItem(row_position, 3, QTableWidgetItem(str(student[3])))   # age

        layout.addWidget(treeview)
        student_popup.setLayout(layout)
        student_popup.exec_()


    def clear_table(self, table_widget):
        """
    Clear the given QTableWidget by removing all rows.

    This method is useful when switching views or refreshing data in the table.

    Parameters:
        table_widget (QTableWidget): The table to be cleared of all rows.
    """
        table_widget.setRowCount(0)

    def setup_search(self, layout):
        """
        Set up search functionality to search through records based on user input.

        Creates a search bar and a button to trigger the search. The search filters through
        student, instructor, or course records, displaying matching entries in the table.

        Parameters:
            layout (QVBoxLayout): The main layout where the search bar and button are added.
        """
        search_layout = QHBoxLayout()

        search_label = QLabel("Search")
        self.search_entry = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_records)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_entry)
        search_layout.addWidget(self.search_button)

        layout.addLayout(search_layout)

    def add_student(self):
        """
    Add a new student to the system.

    This method retrieves the student's name, age, email, and ID from the form,
    and attempts to add the student to the database using the `add_student` function.
    If the student ID already exists in the database, an error message is shown.

    Raises:
        sqlite3.IntegrityError: If the student ID already exists in the database.
    """
        name = self.student_name.text()
        age = self.student_age.text()
        email = self.student_email.text()
        student_id = self.student_id.text()

        try:
            db_add_student(student_id, name, int(age), email)
            QMessageBox.information(self, "Success", "Student added successfully!")
            self.load_data()
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Error", "Student ID already exists.")
    
    def add_instructor(self):
        """
    Add a new instructor to the system.

    This method retrieves the instructor's name, age, email, and ID from the form,
    and attempts to add the instructor to the database using the `add_instructor` function.
    If the instructor ID already exists in the database, an error message is shown.

    Raises:
        sqlite3.IntegrityError: If the instructor ID already exists in the database.
    """
        name = self.instructor_name.text()
        age = self.instructor_age.text()
        email = self.instructor_email.text()
        instructor_id = self.instructor_id.text()

        try:
            db_add_instructor(instructor_id, name, int(age), email)
            QMessageBox.information(self, "Success", "Instructor added successfully!")
            self.load_data()
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Error", "Instructor ID already exists.")

    def add_course(self):
        """
    Add a new course to the system.

    This method retrieves the course's name, ID, and instructor's name from the form.
    It fetches the instructor's ID from the list of instructors and adds the course to the database
    using the `add_course` function. If the instructor is not found, an error message is shown.

    Raises:
        QMessageBox.critical: If the instructor is not found in the system.
    """
        course_name = self.course_name.text()
        course_id = self.course_id.text()
        instructor_name = self.course_instructor.currentText()

        # Fetch the instructor's ID
        instructor = next((i for i in fetch_instructors() if i[1] == instructor_name), None)
        if instructor:
            db_add_course(course_id, course_name, instructor[0])
            QMessageBox.information(self, "Success", "Course added successfully!")
            self.load_data()
        else:
            QMessageBox.critical(self, "Error", "Instructor not found.")

    def register_student(self):
        """
    Register a student for a course.

    This method retrieves the student's name and the course name from the dropdown menus.
    It fetches the corresponding student and course records and attempts to insert a registration
    record into the `registrations` table in the database. If the student is already registered for
    the course, an error message is shown.

    Raises:
        sqlite3.IntegrityError: If the student is already registered for the course.
        QMessageBox.critical: If an invalid student or course is selected.
    """
        student_name = self.registration_student.currentText()
        course_name = self.registration_course.currentText()

        student = next((s for s in fetch_students() if s[1] == student_name), None)
        course = next((c for c in fetch_courses() if c[1] == course_name), None)

        if student and course:
            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO registrations (student_id, course_id) VALUES (?, ?)', (student[0], course[0]))
                conn.commit()
                QMessageBox.information(self, "Success", f"Student {student_name} registered for {course_name}")
            except sqlite3.IntegrityError:
                QMessageBox.critical(self, "Error", "Student is already registered for this course.")
            conn.close()
        else:
            QMessageBox.critical(self, "Error", "Invalid student or course.")


    def assign_instructor(self):
        """
    Assign an instructor to a course.

    This method retrieves the course name and instructor name from the form.
    It fetches the corresponding course and instructor objects from the system
    and assigns the instructor to the course. If the course or instructor is not found,
    an error message is shown.

    Raises:
        QMessageBox.critical: If an invalid instructor or course is selected.
    """
        course_name = self.course_name.text()
        instructor_name = self.course_instructor.currentText()

        course = next((c for c in self.courses if c.course_name == course_name), None)
        instructor = next((i for i in self.instructors if i.name == instructor_name), None)

        if course and instructor:
            course.assign_instructor(instructor)
            QMessageBox.information(self, "Success", f"Instructor {instructor_name} assigned to {course_name}")
        else:
            QMessageBox.critical(self, "Error", "Invalid instructor or course")

    def search_records(self):
        """
    Search and filter student records based on user input.

    This method retrieves the search query entered by the user, clears the current table,
    and populates the table with student records whose ID or name matches the search query.

    Raises:
        None
    """
        search_query = self.search_entry.text().lower()
        self.table.setRowCount(0)  # Clear the table before populating

        for student in self.students:
            # Access tuple values by index: student[0] for student_id, student[1] for name
            if search_query in student[1].lower() or search_query in student[0].lower():
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(student[0]))  # student_id
                self.table.setItem(row_position, 1, QTableWidgetItem(student[1]))  # name
                self.table.setItem(row_position, 2, QTableWidgetItem(student[2]))  # email
                self.table.setItem(row_position, 3, QTableWidgetItem(str(student[3])))  # age

    def save_data(self):
        """
        Save the current student, instructor, and course data to a JSON file.

        The data includes the students, instructors, and courses, and is written
        to a JSON file called 'school_data.json' with the following format:
        - students: List of student records (student_id, name, email, age).
        - instructors: List of instructor records (instructor_id, name, email, age).
        - courses: List of course records, including course details and registered students.
        """
        data = {
            # Access tuple elements by index: student[1] for name, student[3] for email, etc.
            "students": [(s[1], s[2], s[3], s[0]) for s in self.students],  # Assuming tuple (student_id, name, age, email)
            "instructors": [(i[1], i[2], i[3], i[0]) for i in self.instructors],  # Assuming tuple (instructor_id, name, age, email)
            "courses": [
                {
                    "course_id": c[0],  # Assuming tuple (course_id, course_name, instructor_name)
                    "course_name": c[1],
                    "instructor": c[2],
                    "students": [student[0] for student in c[3]] if len(c) > 3 else []  # If course tuple contains student list
                }
                for c in self.courses
            ]
        }
        with open("school_data.json", "w") as f:
            json.dump(data, f, indent=4)

        QMessageBox.information(self, "Data Saved", "Data has been saved successfully.")

    def refresh_data(self):
        """
    Load the saved data from a JSON file and refresh the application tables and comboboxes.

    This method reads data from 'school_data.json' and populates the application with saved students,
    instructors, and courses. It updates the table and comboboxes accordingly. If no saved data is found,
    a warning message is displayed.
    
    Raises:
        FileNotFoundError: If the 'school_data.json' file is not found.
    """
        try:
            with open("school_data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No saved data found.")
            return

        for student_data in data.get("students", []):
            if not any(s.student_id == student_data[3] for s in self.students):  
                student = Student(*student_data)
                self.students.append(student)
                self.update_table(student.student_id, student.name, "Student")

        for instructor_data in data.get("instructors", []):
            if not any(i.instructor_id == instructor_data[3] for i in self.instructors):  
                instructor = Instructor(*instructor_data)
                self.instructors.append(instructor)
                self.update_table(instructor.instructor_id, instructor.name, "Instructor")
                self.update_comboboxes()

        for course_data in data.get("courses", []):
            course_id = course_data.get('course_id')
            course_name = course_data.get('course_name')
            instructor_name = course_data.get('instructor')
            student_ids = course_data.get('students', [])

            instructor = next((i for i in self.instructors if i.name == instructor_name), None)

            if instructor and not any(c.course_id == course_id for c in self.courses):  
                course = Course(course_id, course_name, instructor)

                for student_id in student_ids:
                    student = next((s for s in self.students if s.student_id == student_id), None)
                    if student:
                        course.add_student(student)

                self.courses.append(course)
                self.update_table(course.course_id, course.course_name, "Course")

        QMessageBox.information(self, "Refresh Complete", "New data has been loaded.")

    def update_comboboxes(self):
        """
    Update the values in the comboboxes for students, instructors, and courses.

    This method updates the comboboxes with the latest students, instructors, and courses from the system
    to be used in forms for registration, adding courses, and other operations.
    """
        student_names = [student.name for student in self.students]
        self.registration_student.clear()
        self.registration_student.addItems(student_names)

        instructor_names = [instructor.name for instructor in self.instructors]
        self.course_instructor.clear()
        self.course_instructor.addItems(instructor_names)

        course_names = [course.course_name for course in self.courses]
        self.registration_course.clear()
        self.registration_course.addItems(course_names)

    def update_table(self, id_value, name_value, type_value):
        """
    Update the table with new entries for students, instructors, or courses.

    This method inserts a new row into the table with the provided ID, name, and type (Student, Instructor, or Course).

    Parameters:
        id_value (str): The ID of the entry to add.
        name_value (str): The name of the entry to add.
        type_value (str): The type of the entry (e.g., 'Student', 'Instructor', 'Course').
    """
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(id_value))
        self.table.setItem(row_position, 1, QTableWidgetItem(name_value))
        self.table.setItem(row_position, 2, QTableWidgetItem(type_value))


    def load_data(self):
        """
        Load student, instructor, and course data from the database.

        This method retrieves the latest data from the database and populates
        the table with students and instructors. The combo boxes for student registration
        are also updated with the latest data.
        """
        self.table.setRowCount(0)
        self.students = fetch_students()
        self.instructors = fetch_instructors()
        self.courses = fetch_courses()

        # Ensure the self.students, self.instructors, and self.courses lists are populated correctly
        if not self.students:
            print("No students found in the database.")
        if not self.instructors:
            print("No instructors found in the database.")
        if not self.courses:
            print("No courses found in the database.")

        # Insert students into the table
        for student in self.students:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(student[0]))
            self.table.setItem(row_position, 1, QTableWidgetItem(student[1]))
            self.table.setItem(row_position, 2, QTableWidgetItem(student[3]))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(student[2])))
            self.table.setItem(row_position, 4, QTableWidgetItem("Student"))

        # Insert instructors into the combobox
        self.course_instructor.clear()
        for instructor in self.instructors:
            self.course_instructor.addItem(instructor[1])

        # Insert students into the registration form combobox
        self.registration_student.clear()
        self.registration_course.clear()
        for student in self.students:
            self.registration_student.addItem(student[1])
        for course in self.courses:
            self.registration_course.addItem(course[1])

    def delete_record(self):
        """
    Delete the selected record (student, instructor, or course) from the database.

    This method identifies the selected record in the table, fetches the corresponding data 
    from the database (either a student, instructor, or course), and deletes it. After deletion,
    the table is refreshed with the remaining records.

    Raises:
        QMessageBox.critical: If no record is selected or an error occurs during deletion.
    """
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.critical(self, "Error", "Please select a record to delete.")
            return

        row = selected_items[0].row()
        item_values = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
        id_value = item_values[0]

        student = next((s for s in fetch_students() if s[0] == id_value), None)
        instructor = next((i for i in fetch_instructors() if i[0] == id_value), None)
        course = next((c for c in fetch_courses() if c[0] == id_value), None)

        if student:
            delete_student(id_value)
        elif instructor:
            delete_instructor(id_value)
        elif course:
            delete_course(id_value)

        self.load_data()

    def edit_record(self):
        """
    Edit the selected record (student, instructor, or course) in the database.

    This method retrieves the selected record from the table, checks if it is a student, instructor, 
    or course, and calls the appropriate edit method to allow the user to modify the record.

    Raises:
        QMessageBox.critical: If no record is selected or an error occurs during editing.
    """
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.critical(self, "Error", "Please select a record to edit.")
            return

        row = selected_items[0].row()
        # Check if the item is None before trying to access its text
        item_values = [
            self.table.item(row, col).text() if self.table.item(row, col) is not None else "" 
            for col in range(self.table.columnCount())
        ]
        id_value = item_values[0]

        student = next((s for s in fetch_students() if s[0] == id_value), None)
        instructor = next((i for i in fetch_instructors() if i[0] == id_value), None)
        course = next((c for c in fetch_courses() if c[0] == id_value), None)

        if student:
            self.edit_student(student)
        elif instructor:
            self.edit_instructor(instructor)
        elif course:
            self.edit_course(course)

                
    def edit_student(self, student):
        """
    Edit a student's details in the form.

    This method populates the student form with the details of the selected student and
    allows the user to update the student's information. The "Add Student" button is repurposed 
    to "Update Student" for saving the changes.

    Parameters:
        student (tuple): The student record to be edited.
    """
        self.student_name.setText(student[1])
        self.student_age.setText(str(student[2]))
        self.student_email.setText(student[3])
        self.student_id.setText(student[0])
        self.student_id.setReadOnly(True)
        self.add_student_button.setText("Update Student")
        self.add_student_button.clicked.disconnect()
        self.add_student_button.clicked.connect(lambda: self.update_student(student))

    def update_student(self, student):
        """
    Update the selected student's details in the database.

    This method retrieves the updated student details from the form and updates 
    the student record in the database. The "Update Student" button is reset to "Add Student" 
    after the update is saved.

    Parameters:
        student (tuple): The student record being updated.
    """
        db_update_student(
            self.student_id.text(),
            self.student_name.text(),
            int(self.student_age.text()),
            self.student_email.text()
        )
        self.student_id.setReadOnly(False)
        self.add_student_button.setText("Add Student")
        self.add_student_button.clicked.disconnect()
        self.add_student_button.clicked.connect(self.add_student)
        self.load_data()

    def edit_instructor(self, instructor):
        """
    Edit an instructor's details in the form.

    This method populates the instructor form with the details of the selected instructor and
    allows the user to update the instructor's information. The "Add Instructor" button is repurposed 
    to "Update Instructor" for saving the changes.

    Parameters:
        instructor (tuple): The instructor record to be edited.
    """
        self.instructor_name.setText(instructor[1])
        self.instructor_age.setText(str(instructor[2]))
        self.instructor_email.setText(instructor[3])
        self.instructor_id.setText(instructor[0])
        self.add_instructor_button.setText("Update Instructor")
        self.add_instructor_button.clicked.disconnect()
        self.add_instructor_button.clicked.connect(lambda: self.update_instructor(instructor))

    def update_instructor(self, instructor):
        """
    Update the selected instructor's details in the database.

    This method retrieves the updated instructor details from the input fields, such as name, age, and email,
    and updates the corresponding instructor record in the database. After the update, the form is reset,
    and the "Update Instructor" button is reset to "Add Instructor" to allow further additions of new instructors.

    Parameters:
        instructor (tuple): The instructor record that is being updated.

    Actions:
        - Updates the instructor in the database.
        - Resets the form for adding a new instructor.
        - Reloads the updated data into the UI.
    """
        db_update_instructor(
            self.instructor_id.text(),
            self.instructor_name.text(),
            int(self.instructor_age.text()),
            self.instructor_email.text()
        )
        self.add_instructor_button.setText("Add Instructor")
        self.add_instructor_button.clicked.disconnect()
        self.add_instructor_button.clicked.connect(self.add_instructor)
        self.load_data()

    def edit_course(self, course):
        """
    Edit a course's details in the form.

    This method populates the course form with the details of the selected course (course ID, name, and instructor).
    The "Add Course" button is changed to "Update Course" to allow the user to save the modified details.
    
    Parameters:
        course (tuple): The course record that is being edited.

    Actions:
        - Populates the course form with the selected course's details.
        - Updates the "Add Course" button to "Update Course" for saving the changes.
    """
        self.course_id.setText(course[0])
        self.course_name.setText(course[1])
        self.course_instructor.setCurrentText(course[2])
        self.add_course_button.setText("Update Course")
        self.add_course_button.clicked.disconnect()
        self.add_course_button.clicked.connect(lambda: self.update_course(course))

    def update_course(self, course):
        """
    Update the selected course's details in the database.

    This method retrieves the updated course details from the input fields, such as course ID, name, and instructor,
    and updates the corresponding course record in the database. After the update, the form is reset, and the "Update Course" 
    button is reverted to "Add Course" to allow further additions of new courses.

    Parameters:
        course (tuple): The course record that is being updated.

    Actions:
        - Updates the course in the database.
        - Resets the form for adding a new course.
        - Reloads the updated data into the UI.
    """
        instructor = next((i for i in fetch_instructors() if i[1] == self.course_instructor.currentText()), None)
        db_update_course(
            self.course_id.text(),
            self.course_name.text(),
            instructor[0] if instructor else None
        )
        self.add_course_button.setText("Add Course")
        self.add_course_button.clicked.disconnect()
        self.add_course_button.clicked.connect(self.add_course)
        self.load_data()
