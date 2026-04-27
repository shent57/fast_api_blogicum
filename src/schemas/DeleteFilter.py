from typing import Any  # для указания необязательных полей

from pydantic import BaseModel


class DeleteFilter(BaseModel):
    key: str
    value: Any
