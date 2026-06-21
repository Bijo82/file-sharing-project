import secrets
import string

def otpgenerate(length=6):
    characters = string.ascii_letters+string.digits
    otp = "".join(secrets.choice(characters) for _ in range(length))
    return otp