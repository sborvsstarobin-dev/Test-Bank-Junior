from src.main.api.models.base_model import BaseModel


class AuthLoginRequest(BaseModel):
    username: str
    password: str