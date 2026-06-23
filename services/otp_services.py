import secrets
import string

def otpgenerate(length=6):
    characters = string.ascii_uppercase+string.digits
    otp = "".join(secrets.choice(characters) for _ in range(length))
    return otp