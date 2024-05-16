from ninja import Schema


class TokensWithUser(Schema):
    access_token: str
    refresh_token: str
    user_name: str


class Tokens(Schema):
    access_token: str
    refresh_token: str
