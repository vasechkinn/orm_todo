from database import Base, get_db, engine
from fastapi import (FastAPI,
                     Query,
                     Path,
                     status,
                     HTTPException,
                     Request,
                     Depends,
                     Form
                     )
from sqlalchemy.orm import Session
from fastapi.responses import (
    RedirectResponse,
    HTMLResponse,
)

from routers import api, html
app = FastAPI()
app.include_router(router=api.router)
app.include_router(router=html.router)

@app.on_event('startup')
def startup():
    Base.metadata.create_all(engine)
