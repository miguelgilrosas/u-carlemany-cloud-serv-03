from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.authentication.api.router import router as authentication_router
from app.files.api.router import router as files_router
from app.config import DATABASE_URL, models

description = """
# Universidad Carlemany

## Báchelor de Informática

### Cloud Computing Services

#### Profesor: Ramón Amela
"""

metadata = [
    {
        "name": "Authentication",
        "description": "Description of Authentication"
    },
    {
        "name": "Files",
        "description": "Description of Files"
    }
]

app = FastAPI(title='Activity03', description=description, tags_metadata=metadata)
app.include_router(authentication_router, prefix='/auth', tags=['Authentication'])
app.include_router(files_router, prefix='/files', tags=['Files'])
register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": models},
    generate_schemas=False,
    add_exception_handlers=True,
)
