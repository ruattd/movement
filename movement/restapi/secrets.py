import secrets
import string

SECRET_CHARACTERS = string.ascii_letters + string.digits

def generate_secret(length: int):
    return ''.join(secrets.choice(SECRET_CHARACTERS) for _ in range(length))
