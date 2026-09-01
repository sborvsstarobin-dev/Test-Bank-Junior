from src.main.api.models.base_model import BaseModel

class UserResponse(BaseModel):
    username: str
    role: str

class AuthLoginResponse(BaseModel):
    token: str
    user: UserResponse