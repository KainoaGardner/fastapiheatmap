import jwt

# from jwt.exceptions import InvaliedTokenError
from dotenv.main import load_dotenv
import os


load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
print(JWT_SECRET_KEY)
