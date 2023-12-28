from pydantic import BaseModel

class Zip_file(BaseModel):
    filename: str
    content: str