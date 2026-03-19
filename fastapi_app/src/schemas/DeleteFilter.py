from pydantic import BaseModel
from typing import Any # для указания необязательных полей





class DeleteFilter(BaseModel):
    key: str
    value: Any
