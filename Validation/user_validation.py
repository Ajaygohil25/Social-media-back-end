import re
from datetime import datetime

class Validator:
    def validate_registration_data(self, data):
        validations = {
            "username": self.validate_username(data.get('username')),
            "password": self.validate_password(data.get('password')),
            "bio": self.validate_bio(data.get('bio')),
            "gender": self.validate_gender(data.get('gender')),
            "dateofbirth": self.validate_dateofbirth(data.get('dateofbirth')),
            "contact": self.validate_contact(data.get('contact')),
            "email": self.validate_email(data.get('email')),
        }

        errors = {field: error for field, (valid, error) in validations.items() if not valid}
        return errors
    
    def validate_login_data(self, data):
        validations = {
            "username": self.validate_username(data.get('username')),
            "password": self.validate_password(data.get('password')),
        }

        errors = {field: error for field, (valid, error) in validations.items() if not valid}
        return errors

    def validate_username(self, username):
        if username:
            username_str = str(username)
            if len(username_str) < 2:
                return False, "Username must be at least 2 characters long."
            return True, ""
        return False, "Username is required."

    def validate_password(self, password):
        if password:
            if not re.match(r'^(?=.*\d).{8,}$', password):
                return False, "Password must be at least 8 characters long and include at least one number."
            return True, ""
        return False, "Password is required."

    def validate_bio(self, bio):
        if bio:
            return True, ""
        return False, "Bio is required."

    def validate_gender(self, gender):
        if gender in ['male', 'female', 'other']:
            return True, ""
        return False, "Gender must be 'male', 'female', or 'other'."

    def validate_dateofbirth(self, dateofbirth):
        if dateofbirth:
            try:
                datetime.strptime(dateofbirth, '%Y-%m-%d').date()
                return True, ""
            except ValueError:
                return False, "Date of birth must be in YYYY-MM-DD format."
        return False, "Date of birth is required."

    def validate_contact(self, contact):
        if contact:
            contact_str = str(contact)
            contact_regex = re.compile(r'^[0-9]+$')
            if not bool(re.match(contact_regex, contact_str)):
                return False, "Contact must be digits."
            elif len(contact_str) < 10:
                return False, "Contact must be 10 digits long."
            return True, ""
        return False, "Contact is required."

    def validate_email(self, email):
        if email:
            email_str = str(email)
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_str):
                return False, "Invalid email format."
            return True, ""
        return False, "Email is required."

