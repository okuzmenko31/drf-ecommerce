def get_username_from_email(email: str):
    username = email.split('@')
    return username[0]
