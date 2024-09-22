# School Management System

The School Management System has two versions, each stored in a separate file. One version is connected to a database (SQLite), and the other uses JSON files for data storage.

## Running the Application

To run the application, follow these steps:

1. Open a terminal (CMD) and navigate to the directory containing `main.py`.
2. Run the application by typing:
```bash
python main.py
Or
python3 main.py
```
Upon starting, you'll be prompted to choose between two GUI frameworks:

- **Tkinter**
- **PyQt5**

After selecting your preferred GUI, a window will open displaying the School Management System interface.

## Features

The School Management System allows you to manage **students**, **courses**, and **instructors**. Based on the version you're using, the data will either be stored in an SQLite database or in a JSON file.

### Key Functions

1. **Add Students, Courses, and Instructors**
   - **Add New Entries:** You can add new students, courses, and instructors to the system.
   - **Assign Instructors:** When adding a course, you must assign an instructor using a dropdown menu containing previously added instructors.
   - **Register Students for Courses:** When registering a student for a course, you'll select from available courses using a dropdown menu.

2. **Search Functionality**
   - **Easy Search:** The system allows you to search for instructors, courses, and students easily.

3. **Edit and Delete Records**
   - **Edit Records:** You can edit any existing records.
   - **Delete Records:** You can delete any existing records.
   - **ID Integrity:** *Important:* Once an ID (student, instructor, or course ID) is assigned, it cannot be edited.

4. **Refresh Data**
   - **Automatic Loading:** Data is automatically loaded.
   - **Manual Refresh:** If any changes occur, you can manually refresh the data using the **Refresh Data** button.

5. **Save Data**
   - **Save Changes:** After making any additions or changes, it is crucial to click the **Save Data** button to store the data to the database or JSON file.
   - **Important Note:** The **Save Data** function is vital to ensure all changes are stored in the database or JSON file.

6. **Export to CSV (JSON Version Only)**
   - **CSV Export:** The system includes a feature to export your data to a CSV file when using the JSON storage option.
   - **Availability:** The **Export to CSV** feature is available only in the JSON file version.

## Important Notes

- **Data Integrity:** Editing the ID of any student, instructor, or course is not allowed to maintain data integrity.
- **Save Data:** Always use the **Save Data** function to ensure all changes are properly stored.
- **CSV Export:** Available exclusively for the JSON storage version.

This system provides a simple yet robust way to manage students, courses, and instructors, with easy data handling through either SQLite or JSON files.

