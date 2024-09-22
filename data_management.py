# data_management.py
import json
import re

def validate_email(email):
    """
    Validate if the provided email follows a proper email format.

    This function uses a regular expression to check if the given email has a valid format,
    which includes characters before and after the '@' symbol and a domain.

    Parameters:
        email (str): The email address to validate.

    Returns:
        bool: True if the email format is valid, False otherwise.
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_age(age):
    """
    Validate if the provided age is non-negative.

    This function checks if the provided age is greater than or equal to zero.

    Parameters:
        age (int): The age to validate.

    Returns:
        bool: True if the age is valid (non-negative), False otherwise.
    """
    return age >= 0

def save_data(filename, data):
    """
    Save data to a JSON file.

    This function takes a dictionary or list and saves it as a JSON file with the specified filename.

    Parameters:
        filename (str): The name of the file where the data will be saved.
        data (dict or list): The data to be saved into the file.

    Actions:
        - Writes the data to the file in JSON format.
    """
    with open(filename, 'w') as file:
        json.dump(data, file)


def load_data(filename):
    """
    Load data from a JSON file.

    This function reads the specified file and loads the data as a dictionary. If the file does not
    exist or contains invalid JSON, it handles the errors gracefully and returns an empty dictionary.

    Parameters:
        filename (str): The name of the file to load data from.

    Returns:
        dict: The loaded data if the file is valid, or an empty dictionary if the file is not found 
        or contains invalid JSON.
    
    Exceptions:
        - Handles FileNotFoundError if the file doesn't exist.
        - Handles json.JSONDecodeError if the file contains invalid JSON.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found. Returning an empty dictionary.")
        return {}
    except json.JSONDecodeError:
        print(f"File {filename} is empty or contains invalid JSON. Returning an empty dictionary.")
        return {}
