import re

def validate_username(username):
    """
    Validate a name.

    Parameters:
    - name (str): The name to validate.

    Returns:
    - bool: True if the name is valid, False otherwise.
    """
    # Regular expression to match only alphabets and spaces
    pattern = "^[A-Za-z ]+$"
    
    # Check if the name matches the pattern
    if re.match(pattern, username):
        if len(username) > 3 :
            return True
    else:
        return False


def validate_password(password, retype):
    """
    Validate a password and its retype.

    Parameters:
    - password (str): The password to validate.
    - retype (str): The retyped password to validate.

    Returns:
    - bool: True if both passwords are valid and match, False otherwise.
    """
    # Check if passwords are not empty and match
    if password and retype and password == retype:
        # Check if password meets criteria (e.g., length, complexity)
        if len(password) >= 8:  # Adjust as per your requirements
            return True
        else:
            print("Password should be at least 8 characters long.")
            return False
    else:
        print("Passwords do not match.")
        return False

