import uvicorn
from fastapi import FastAPI
import zipfile
import io

from model import Zip_file

app = FastAPI()

@app.get("/")
def home():
    return {"Message": "Hello World"}

@app.post("/readzip/")
async def read_zip(file: Zip_file):
    zip_file_like = io.StringIO(file['content'])
    #info = zipfile.ZipInfo(zip_file_like, 'r')
    return zip_file_like.read()

if __name__ == "__main__":
    uvicorn.run("lama_secours:app", reload=True)
