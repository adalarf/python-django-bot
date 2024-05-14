from app.internal.auth.db.models import IssuedToken
import abc


class IAuthRepository(abc.ABC):
    @abc.abstractmethod
    def create_issued_token(self, user, refresh_token):
        pass

    @abc.abstractmethod
    def get_issued_token(self, refresh_token) -> IssuedToken:
        pass

    @abc.abstractmethod
    def revoke_all_tokens_by_user_id(self, user_id):
        pass

    @abc.abstractmethod
    def revoke_token(self, token):
        pass


class AuthRepository(IAuthRepository):
    def create_issued_token(self, user, refresh_token):
        IssuedToken.objects.create(user=user, jti=refresh_token)

    def get_issued_token(self, refresh_token) -> IssuedToken:
        return IssuedToken.objects.filter(jti=refresh_token).first()

    def revoke_all_tokens_by_user_id(self, user_id):
        IssuedToken.objects.filter(user__id=user_id).update(revoked=True)

    def revoke_token(self, token):
        IssuedToken.objects.filter(jti=token).update(revoked=True)
