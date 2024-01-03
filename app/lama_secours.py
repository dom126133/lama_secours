import uvicorn
import os
import json
import logging
from fastapi import FastAPI, File, UploadFile
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
from uuid import uuid4
from datetime import datetime

from model import Uploaded_file
from output import pdf

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

app = FastAPI()

@app.get("/")
def home():
    return {"Message": "Hello World"}

@app.get("/help")
def help():
    return { "example": "http://127.0.0.1:8000/tasks4shift/?filename=384bd982-aa8c-4147-b122-5d4b863fa169.zip&shiftname=G1_GVE_22-12-2023_08-29-53.json"}

@app.post("/uploadzip/")
async def upload_zip(file: UploadFile):
    try:
        content = file.file.read()
    except Exception:
        logging.warning(f"Error when uploading file!")
        return {"message": "Error with uploading file!"}
    finally:
        file.file.close()
    
    filename = f"{str(uuid4())}.zip"
    with open(f'tmp/{filename}', 'wb') as f:
        f.write(content)

    return {"filename": filename}

@app.get("/uploadedfile", response_model=list[Uploaded_file])
async def uploaded_file():
    file_list = os.scandir("tmp")
    file_dict = {}
    files = []
    for file in file_list:
        c_time = datetime.fromtimestamp(os.path.getctime(file))
        c_time_formated = c_time.strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"Filename: {file.name}, Creation_date: {c_time_formated}")
        files.append({"filename": file.name, "creation_date": c_time_formated})
    
    return files

@app.get("/shifts/{filename}")
async def shifts(filename):
    with ZipFile(f'tmp/{filename}', 'r') as zipfile:
        shifts = zipfile.namelist()
    
    return shifts

@app.get("/tasks4shift/")
async def tasks4shift(filename, shiftname):
    logging.debug(f"In tasks4shift with {filename} and {shiftname}")
    with ZipFile(f'tmp/{filename}', 'r') as zipfile:
        with zipfile.open(shiftname) as shift:
            shift_task_list = json.load(shift)

    tasks = pd.json_normalize(shift_task_list['taskDefinitions'])
    tasks.set_index('id', inplace=True)
    tasks_cleaned = tasks.drop(['version',\
                                'name',\
                                'unit',\
                                'onDemand',\
                                'allowedStartTime',\
                                'duration',\
                                'schedule.startDate',\
                                'schedule.endDate',\
                                'schedule.expression',\
                                'auditData.createdBy',\
                                'auditData.createdTime',\
                                'auditData.lastModifiedBy',\
                                'auditData.lastModifiedTime'],\
                                axis=1)
    
    pdf(tasks_cleaned)
    #print(tasks_cleaned)




if __name__ == "__main__":
    uvicorn.run("lama_secours:app", reload=True)
