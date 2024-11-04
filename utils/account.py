import jwt
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')

def generate_jwt(user_id):
    if isinstance(user_id, uuid.UUID):
        user_id = str(user_id)
    
    payload = {
        'user_id': user_id,
    }
    token = jwt.encode(payload, secret_key, algorithm=algorithm)

    return "Bearer " + token