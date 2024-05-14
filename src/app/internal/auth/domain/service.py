from app.internal.auth.db.models import IssuedToken
from datetime import datetime, timedelta
import jwt
from config import settings
from app.internal.auth.db.repositories import AuthRepository, IAuthRepository


class AuthService:
    def __init__(self, auth_repository: IAuthRepository):
        self._auth_repository = auth_repository

    def generate_access_token(self, user_id):
        access_token_payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(days=0, minutes=5),
            "iat": datetime.utcnow(),
        }
        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256")
        return access_token

    def generate_refresh_token(self, user_id):
        refresh_token_payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(days=7),
            "iat": datetime.utcnow(),
        }
        refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm="HS256")
        return refresh_token

    def get_payload(self, token):
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

    def create_issued_token(self, user, refresh_token):
        self._auth_repository.create_issued_token(user, refresh_token)

    def get_issued_token(self, refresh_token) -> IssuedToken:
        return self._auth_repository.get_issued_token(refresh_token)

    def get_user_id_by_token(self, token):
        payload = self.get_payload(token.jti)
        return int(payload["sub"])

    def is_token_expired(self, token):
        payload = self.get_payload(token.jti)
        expiration_date = datetime.fromtimestamp(payload["exp"])
        return expiration_date <= datetime.utcnow()

    def revoke_all_tokens_by_user_id(self, user_id):
        self._auth_repository.revoke_all_tokens_by_user_id(user_id)

    def revoke_token(self, token):
        self._auth_repository.revoke_token(token)


def get_auth_service() -> AuthService:
    return AuthService(AuthRepository())
