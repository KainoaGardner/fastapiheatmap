from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password, hashed_password):
    return bcrypt_context.verify(password, hashed_password)


def get_password_hash(password):
    return bcrypt_context.hash(password)
