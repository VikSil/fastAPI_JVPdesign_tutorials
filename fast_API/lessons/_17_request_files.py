from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.post('/files')
async def create_file(file: bytes = File(..., description='A file as a bytestream')):

    return {'file': len(file)}


@router.post('/uploadfile')
async def create_upload_file(file: UploadFile):  # this will be an object with properties

    contents = await file.read()
    print(contents)
    return {'filename': file.filename}


# docs and code on spooled files:
# https://github.com/search?q=repo%3Aencode%2Fstarlette+spooled&type=code


@router.post('/mixed_files')
async def mixed_files(file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)):

    return {'file_size': len(file), 'token': token, 'fileb_content_type': fileb.content_type}


@router.post('/multifilesfiles')
async def create_file(files: list[bytes] = File(...)):

    return {'file_sizes': [len(file) for file in files]}


@router.post('/multiuploadfile')
async def create_upload_file(files: list[UploadFile] = File(...)):

    return {'filenames': [file.filename for file in files]}


# Example of rendering an HTML form
@router.get('/fileform')
async def fileform():
    content = '''
        <body>
        <form action = "/files" enctype = "multipart/form-data" method = "post">
        <input name = "files" type = "file" multiple>
        <input type = "submit">
        </form>
        <form action = "/uploadfiles" enctype = "multipart/form-data" method = "post">
        <input name = "files" type = "file" multiple>
        <input type = "submit">
        </form>
        </body>
'''

    return HTMLResponse(content=content)
