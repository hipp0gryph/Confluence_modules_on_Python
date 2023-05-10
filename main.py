# psycopg2 need for sqlalchemy postgres connect
import psycopg2

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import db
import htmls
from db import get_session
import uvicorn

from cruds import crud_group, crud_achievements, crud_marks, crud_users

print("Ver psycopg:", psycopg2.__version__)
app = FastAPI(title="Confluence Backend Service", version="0.1.0")
db.init()
app.mount("/achieve_files", StaticFiles(directory="/app/templates/achieve_files", html=False), name="achieve_files")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crud_users.router)
app.include_router(crud_marks.router)
app.include_router(crud_group.router)
app.include_router(crud_achievements.router)
app.include_router(htmls.router)


@app.post('/session/fix', tags=['health'])
def fix_session():
    db_session = get_session()
    db_session.rollback()


@app.get('/', tags=['health'])
def health():
    return 'Service is alive'


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
