from fastapi import FastAPI

# this will show up at the top of the docs
description = """
This app does awesome stuff.

## Items

You can **read items**.

## Users

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

tags_metadata = [
    dict(name='users', description='This will show up next to the users tag'),
    dict(
        name='items',
        description='This will show up next to the items tag',
        externalDocs=dict(description='External docs about the items', url='https://ww.jvp.design'),
    ),
]

app = FastAPI(
    title='This app',
    description=description,
    version='0.0.1',
    terms_of_service='http://example.com/tems',
    contact=dict(name='Deadpool', url='http://x-force.example.com/contact', email='dp@x-force.exmaple.com'),
    license_info=dict(name='Apache 2.0', url='https://apache.org/licenses/LICENSE-2.0.html'),
    openapi_tags=tags_metadata,
    openapi_url='/api/v1/openapi.json', # docs in json format
    docs_url='/hello-world', # moves the /docs route
    redoc_url=None # removes the /redoc route
)


@app.get('/users', tags=['users'])
async def get_users():
    return [dict(name='Harry'), dict(name='Hermione')]


@app.get('/items', tags=['items'])
async def read_items():
    return [dict(name='wand'), dict(name='flying broom')]
