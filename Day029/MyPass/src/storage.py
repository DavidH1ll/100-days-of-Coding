class PasswordStorage:
    def __init__(self, filename='passwords.txt'):
        self.filename = filename

    def add_password(self, website, username, password):
        with open(self.filename, 'a') as file:
            file.write(f"{website} | {username} | {password}\n")

    def retrieve_passwords(self):
        passwords = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    passwords.append(line.strip().split(' | '))
        except FileNotFoundError:
            return passwords  # Return empty list if file does not exist
        return passwords

    def find_password(self, website):
        passwords = self.retrieve_passwords()
        for entry in passwords:
            if entry[0] == website:
                return entry
        return None  # Return None if website not found

    def delete_password(self, website):
        passwords = self.retrieve_passwords()
        with open(self.filename, 'w') as file:
            for entry in passwords:
                if entry[0] != website:
                    file.write(f"{entry[0]} | {entry[1]} | {entry[2]}\n")