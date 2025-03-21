from fastapi import FastAPI

from app.authentication.router import router as authentication_router
from app.files.router import router as files_router

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

app = FastAPI(title='Activity02', description=description, tags_metadata=metadata)
app.include_router(authentication_router, prefix='/auth', tags=['Authentication'])
app.include_router(files_router, prefix='/files', tags=['Files'])
