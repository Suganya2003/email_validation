from email_validator import validate_email, EmailNotValidError

def is_valid_email(email):
    try:
        # Validate email address
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


# is_valid_syntax = is_valid_email("sathish.personal18@gmail.com")
# print(f" {is_valid_syntax}")