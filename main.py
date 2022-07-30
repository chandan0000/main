from typing import Union

from fastapi import FastAPI, File, UploadFile

app = FastAPI()
app = FastAPI()
@app.post("/")
def read_root(file:UploadFile=File(...)):
    
    return {'file_name':file.filename}