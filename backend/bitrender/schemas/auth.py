from pydantic import BaseModel as BaseSchema


class TokenData(BaseSchema):
    username: str
    scopes: list[str]
