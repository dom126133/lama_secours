import uvicorn
import os
from fastapi import FastAPI, File, UploadFile
from zipfile import ZipFile
from io import BytesIO
from uuid import uuid4
from model import Zip_file
from datetime import datetime

app = FastAPI()

@app.get("/")
def home():
    return {"Message": "Hello World"}

@app.post("/uploadzip/")
async def upload_zip(file: UploadFile):
    try:
        #content = BytesIO(file.file.read())
        content = file.file.read()
    except Exception:
        return {"message": "Error with uploading file!"}
    finally:
        file.file.close()
    
    #zip_file = ZipFile(content)
    filename = f"{str(uuid4())}.zip"
    with open(f'tmp/{filename}', 'wb') as f:
        f.write(content)

    return {"filename": filename}

@app.get("/uploadedfile")
async def uploaded_file():
    file_list = os.scandir("tmp")
    for file in file_list:
        c_time = datetime.fromtimestamp(os.path.getctime(file))
        print(f"{file.name}: {c_time.strftime('%Y-%m-%d %H:%M:%S')}")
if __name__ == "__main__":
    uvicorn.run("lama_secours:app", reload=True)
