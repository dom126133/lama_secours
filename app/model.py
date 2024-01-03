from pydantic import BaseModel
from typing import List

class Uploaded_file(BaseModel):
    filename: str
    creation_date: str