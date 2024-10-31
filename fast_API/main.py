from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from lessons import (
    _01_get_post_put,
    _02_path_parameters,
    _03_query_parameters,
    _04_request_body,
    _05_type_conversion,
    _07_multiple_body_params,
    _08_body_fields,
    _09_body_nested_models,
    _10_body_example,
    _11_extra_data_types,
    _12_cookies_and_headers,
    _13_response_model,
    _14_union_types,
    _15_response_status_codes,
    _16_form_fields,
    _17_request_files,
    _20_docs_configuration,
    _21_json_manipulations,
    _22_dependencies,
    _23_class_dependencies,
    _24_subdependencies,
    _25_depencies_in_path,
    # _26_security, # cannot work together with _27_security_with_JWT
    _27_security_with_JWT,
    _31_background_tasks,
)
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time

app = FastAPI()

app.include_router(_01_get_post_put.router)
app.include_router(_02_path_parameters.router)
app.include_router(_03_query_parameters.router)
app.include_router(_04_request_body.router)
app.include_router(_05_type_conversion.router)
app.include_router(_07_multiple_body_params.router)
app.include_router(_08_body_fields.router)
app.include_router(_09_body_nested_models.router)
app.include_router(_10_body_example.router)
app.include_router(_11_extra_data_types.router)
app.include_router(_12_cookies_and_headers.router)
app.include_router(_13_response_model.router)
app.include_router(_14_union_types.router)
app.include_router(_15_response_status_codes.router)
app.include_router(_16_form_fields.router)
app.include_router(_17_request_files.router)
app.include_router(_20_docs_configuration.router)
app.include_router(_21_json_manipulations.router)
app.include_router(_22_dependencies.router)
app.include_router(_23_class_dependencies.router)
app.include_router(_24_subdependencies.router)
app.include_router(_25_depencies_in_path.router)
# app.include_router(_26_security.router) # cannot work together with _27_security_with_JWT
app.include_router(_27_security_with_JWT.router)
app.include_router(_31_background_tasks.router)


# app.mount('/static', StaticFiles(directory='./lessons/static'), name='static')

# ========================================
#  For lesson 19 on Exception handling
# ========================================

# items = {'foo': 'This is foo'}


# @app.get('/error_items')
# async def read_item(item_id: str):

#     if item_id not in items:
#         raise HTTPException(status_code=404, detail='Item not found', headers={'X-Errors': 'There was an error'})

#     return {'item': items[item_id]}


# class UnicornException(Exception):
#     def __init__(self, name: str):
#         self.name = name


# # APIRouter does not have exception_handler, only FastAPI does
# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):

#     return JSONResponse(status_code=418, content={'message': f'Ooops! {exc.name} happened'})


# @app.get('/unicorns/{name}')
# async def read_unicorns(name: str):

#     if name == 'yolo':
#         raise UnicornException(name=name)

#     return {'unicorn_name': name}


# # # makes type validation errors more human readable
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse(str(exc), status_code=400)


# @app.get('/validation_items/{item_id}')
# async def read_validation_items(item_id: int):

#     if item_id == 3:
#         raise HTTPException(status_code=418, detail='Nope, three is not allowed')

#     return {'item_id': item_id}


# # another way to override the HTTP errors
# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# # another way to override the HTTP errors
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):

#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({'detail': exc.errors(), 'body': exc.body}),
#     )


# class Item(BaseModel):
#     title: str
#     size: int


# @app.post('/validated_items')
# async def create_item(item: Item):
#     return item


# # another way to override the HTTP errors
# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request, exc):
#     print(f'Exception happened! {repr(exc)}')

#     return await http_exception_handler(request, exc)


# # another way to override request validation errors
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     print(f'Exception happened {exc}')

#     return await request_validation_exception_handler(request, exc)


# @app.get('/valid_items/{item_id}')
# async def read_items(item_id: int):

#     if item_id == 3:
#         raise HTTPException(status_code=418, detail='We do not like three')

#     return {'item_id': item_id}


# ========================================
#  For lesson 28 on Middleware and CORS
# ========================================


class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)

        return response


origins = [
    'http://localhost:8011',
    'http://127.0.0.1:8011',
]

# APIRouter does not have add_middleware, only FastAPI does
app.add_middleware(MyMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=origins)


@app.get('/middleware_blah')
async def blah():
    return {'hello': 'world'}


# ========================================
#  For lesson 33 on Static files
# ========================================

#  StaticFiles cannot be mounted onto an APIRouter, only onto FastAPI
app.mount('/static', StaticFiles(directory='./static'), name='static')
