import re

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    if re.match(pattern, email):
        print(f"{email} is valid")
    else:
        print(f"{email} is invalid")

validate_email("likhitha@gmail.com")
validate_email("namitha-email")