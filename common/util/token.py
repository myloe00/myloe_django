import jwt
import time
from myloe_django.settings import SECRET_KEY
from myloe_django.settings import TOKEN_EXPIRED_TIME
jwt.ExpiredSignatureError


class JWTToken:
    @staticmethod
    def get_token(payloads: dict, time_out=TOKEN_EXPIRED_TIME):
        payloads.setdefault('iat', time.time())
        payloads.setdefault('exp', time.time() + time_out)
        return jwt.encode(payloads, SECRET_KEY)

    @staticmethod
    def decrypt_token(token):
        return jwt.decode(token, SECRET_KEY, algorithms='HS256')


if __name__ == '__main__':
    x = JWTToken.get_token({"xx": 1}, time_out=2)
    time.sleep(3)
    JWTToken.decrypt_token(x)
