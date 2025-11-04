class Validator:
    @staticmethod
    def validate_email(email):
        """Basic email validation"""
        return "@" in email and "." in email.split("@")[-1]

    @staticmethod
    def validate_website(website):
        """Check if website name is not empty"""
        return len(website.strip()) > 0

    @staticmethod
    def validate_password(password):
        """Check if password is not empty"""
        return len(password.strip()) > 0

    @staticmethod
    def validate_all(website, email, password):
        """Validate all fields"""
        return (Validator.validate_website(website) and 
                Validator.validate_email(email) and 
                Validator.validate_password(password))