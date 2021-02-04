from pydantic import BaseModel

from bitbitbot.models import Role


class Command(BaseModel):
    name: str
    message: str
    permission: Role = Role.VIEWER
