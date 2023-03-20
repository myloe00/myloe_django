import jwt
import time
from myloe_django.settings import SECRET_KEY
from myloe_django.settings import TOKEN_EXPIRED_TIME
from django.core.serializers.json import DjangoJSONEncoder


class JWTToken:
    @staticmethod
    def get_token(payloads: dict, time_out=TOKEN_EXPIRED_TIME):
        payloads.setdefault('iat', time.time())
        payloads.setdefault('exp', time.time() + time_out)
        return jwt.encode(payloads, SECRET_KEY, json_encoder=DjangoJSONEncoder)

    @staticmethod
    def decrypt_token(token):
        token_data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        return token_data

    @classmethod
    def refresh_token(cls, token, deadline_time=10):
        """
            如果距离过期时间不足deadline_time，则返回一个新的token
        """
        payloads = cls.decrypt_token(token)
        token = cls.refresh_token_by_payloads(payloads)
        return token

    @classmethod
    def refresh_token_by_payloads(cls, payloads, deadline_time=10):
        """
            如果距离过期时间不足deadline_time，则返回一个新的token
        """
        token = None
        exp = payloads.get('exp')
        iat = payloads.get('iat')
        if exp - time.time() < deadline_time:
            # 如果距离过期时间不足deadline_time，则刷新token
            interval = exp - iat
            payloads['exp'] = exp + interval
            token = cls.get_token(payloads)
        return token


if __name__ == '__main__':
    x = JWTToken.get_token({"xx": 1}, time_out=2)
    time.sleep(3)
    JWTToken.decrypt_token(x)
