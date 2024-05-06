from app.internal.models.issued_token import IssuedToken
from datetime import datetime, timedelta
import jwt
from config import settings


def generate_access_token(user_id):
    access_token_payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=0, minutes=5),
        "iat": datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256")
    return access_token


def generate_refresh_token(user_id):
    refresh_token_payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm="HS256")
    return refresh_token


def get_payload(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])


def create_issued_token(user, refresh_token):
    IssuedToken.objects.create(user=user, jti=refresh_token)


def get_issued_token(refresh_token) -> IssuedToken:
    return IssuedToken.objects.filter(jti=refresh_token).first()


def get_user_id_by_token(token):
    payload = get_payload(token.jti)
    return int(payload["sub"])


def is_token_expired(token):
    payload = get_payload(token.jti)
    expiration_date = datetime.fromtimestamp(payload["exp"])
    return expiration_date <= datetime.utcnow()


def revoke_all_tokens_by_user_id(user_id):
    IssuedToken.objects.filter(user__id=user_id).update(revoked=True)


def revoke_token(token):
    IssuedToken.objects.filter(jti=token).update(revoked=True)
