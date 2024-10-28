# global libraries
from fastapi import FastAPI

# local modules
from lessons import (
    _01_get_post_put,
    _02_path_parameters,
    _03_query_parameters,
    _04_request_body,
    _05_type_conversion,
    _07_multiple_body_params,
    _08_body_fields,
    _09_body_nested_models
)


app = FastAPI()

app.include_router(_01_get_post_put.router)
app.include_router(_02_path_parameters.router)
app.include_router(_03_query_parameters.router)
app.include_router(_04_request_body.router)
app.include_router(_05_type_conversion.router)
app.include_router(_07_multiple_body_params.router)
app.include_router(_08_body_fields.router)
app.include_router(_09_body_nested_models.router)
