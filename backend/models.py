
from pydantic import BaseModel
from typing import List

class CategoryInfo(BaseModel):
    title: str
    description: str
    source: str
