import uvicorn
from fastapi import FastAPI, File, UploadFile
import zipfile
import io

from model import Zip_file

app = FastAPI()

@app.get("/")
def home():
    return {"Message": "Hello World"}

@app.post("/readzip/")
async def read_zip(file: UploadFile):
    content = file.read()
    return content
if __name__ == "__main__":
    uvicorn.run("lama_secours:app", reload=True)
