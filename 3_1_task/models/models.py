from typing import Annotated
from pydantic import BaseModel, Field, field_validator, StringConstraints


class UserCreate(BaseModel):
    name: str
    email: Annotated[str, StringConstraints(pattern=r"^[^@]+@[^@]+\.[^@]+$")]
    age: Annotated[int, Field(gt=0)] = 18
    is_subscribed: bool = False