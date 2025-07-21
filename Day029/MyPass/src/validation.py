class Validator:
    def __init__(self):
        pass

    def validate_non_empty(self, field_value):
        """Check if the input field is not empty."""
        return bool(field_value.strip())

    def validate_password_complexity(self, password):
        """Check if the password meets complexity requirements."""
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char in "!@#$%^&*()-_=+" for char in password):
            return False
        return True

    def validate_fields(self, website, username, password):
        """Validate all input fields."""
        if not self.validate_non_empty(website):
            return "Website field cannot be empty."
        if not self.validate_non_empty(username):
            return "Username field cannot be empty."
        if not self.validate_non_empty(password):
            return "Password field cannot be empty."
        if not self.validate_password_complexity(password):
            return "Password must be at least 8 characters long and include a mix of letters, numbers, and symbols."
        return True