import sys

def main():
    """
    Main function to select and launch a GUI framework.

    This function presents the user with a choice between two GUI frameworks: Tkinter and PyQt5. 
    Based on the user's input, it initializes the selected GUI framework and runs the corresponding 
    School Management System application.

    Actions:
        - If the user selects Tkinter (choice "1"), it imports Tkinter and runs the Tkinter-based 
          School Management System application.
        - If the user selects PyQt5 (choice "2"), it imports PyQt5 and runs the PyQt5-based 
          School Management System application.
        - If the user provides an invalid input, the program prints an error message and exits.

    Notes:
        - The Tkinter GUI is run using `tk.Tk()` as the root window.
        - The PyQt5 GUI is run using `QApplication(sys.argv)` to manage application arguments and execution.

    Input:
        - User selects a GUI framework by entering "1" for Tkinter or "2" for PyQt5.

    Exceptions:
        - The program exits if the user provides an invalid choice.
    """
    print("Choose GUI framework:")
    print("1. Tkinter")
    print("2. PyQt5")
    
    choice = input("Enter the number of the framework you'd like to use: ")
    
    if choice == "1":
        import tkinter as tk
        from tkintergui import SchoolManagementSystemApp as TkinterApp

        root = tk.Tk()
        app = TkinterApp(root)
        root.mainloop()
    
    elif choice == "2":
        from PyQt5.QtWidgets import QApplication
        from pyqtgui import SchoolManagementSystemApp as PyQtApp

        app = QApplication(sys.argv)
        window = PyQtApp()
        window.show()
        sys.exit(app.exec_())

    else:
        print("Invalid choice. Exiting.")

if __name__ == '__main__':
    main()
