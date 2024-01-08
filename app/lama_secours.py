import uvicorn
import os
import json
import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, request
from markupsafe import escape
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
import numpy as np
from uuid import uuid4
from datetime import datetime

from model import Uploaded_file
from output import pdf
from flask_modules import blueprint_index

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

flask_app = Flask(__name__)

flask_app.register_blueprint(blueprint_index, url_prefix='/')


app = FastAPI()

@app.get("/v2")
def home():
    return {"Message": "Welcome in Vigogne, the lama substitute"}

@app.get("/v2/help")
def help():
    return { "example": "http://127.0.0.1:8000/tasks4shift/?filename=384bd982-aa8c-4147-b122-5d4b863fa169.zip&shiftname=G1_GVE_22-12-2023_08-29-53.json"}

@app.post("/v2/uploadzip/")
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

@app.get("/v2/uploadedfile", response_model=list[Uploaded_file])
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

@app.get("/v2/shifts/{filename}")
async def shifts(filename):
    with ZipFile(f'tmp/{filename}', 'r') as zipfile:
        shifts = zipfile.namelist()
    
    return shifts

@app.get("/v2/tasks4shift/")
async def tasks4shift(filename, shiftname):
    logging.debug(f"In tasks4shift with {filename} and {shiftname}")
    # open zipfile and extract the json file corresponding to shiftname
    with ZipFile(f'tmp/{filename}', 'r') as zipfile:
        with zipfile.open(shiftname) as shift:
            shift_task_list = json.load(shift)

    # convert the json value to pandas dataframe
    tasks = pd.json_normalize(shift_task_list['taskDefinitions'])
    # set index to the id which is defined in LAMA ans is unique
    tasks.set_index('id', inplace=True)
    # remove unnecessary column in the pandas dataframe
    tasks_cleaned = tasks.drop(['version',\
                                'name',\
                                'unit',\
                                'commands',\
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
    # reorder the columns
    tasks_ordered = tasks_cleaned.loc[:,['intendedStartTime','zoneId','description']]
    # convert the pandas dataframe to a list
    task_list = np.array(tasks_ordered).tolist()
    # insert the header for the columns
    task_list.insert(0,['Start time', 'Locale', 'Description'])

    t1 = pdf(task_list)

    return t1


app.mount('/v1', WSGIMiddleware(flask_app))

if __name__ == "__main__":
    uvicorn.run("lama_secours:app", reload=True)
