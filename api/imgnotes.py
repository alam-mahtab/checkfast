import os
import shutil
import uuid
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

config = {
	'WORK_DIR':'data/'
}

@router.post("/upload/files/")
async def create_upload_files(files: List[UploadFile] = File(...)):
	# base directory 
    WORK_DIR = Path(config.get('WORK_DIR'))  # UUID to prevent file overwrite
    REQUEST_ID = Path(str(uuid.uuid4())[:8])
    # 'beautiful' path concat instead of WORK_DIR + '/' + REQUEST_ID
    WORKSPACE = WORK_DIR / REQUEST_ID
    if not os.path.exists(WORKSPACE):
    	# recursively create workdir/unique_id
	    os.makedirs(WORKSPACE)
    # iterate through all uploaded files
    for file in files:
	    FILE_PATH = Path(file.filename)
	    WRITE_PATH = WORKSPACE / FILE_PATH
	    with open(str(WRITE_PATH) ,'wb') as myfile:
		    contents = await file.read()
		    myfile.write(contents)
	# return local file paths
    return {"file_paths": [str(WORKSPACE)+'/'+file.filename for file in files]}


@router.get("/upload")
async def main():
	content = """
<body>
<form action="/upload/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
	"""
	return HTMLResponse(content=content)


@router.get("/ping")
def ping():
	return {"message": "pong"}