import uvicorn

from fastapi import FastAPI, Depends
from api.auth import crud
from api.database import get_db


app = FastAPI(title='SCB API', deescription='backend for prayer request and testimony', version='1.0.0')

@app.get("/")
async def read_root():
    return ('Welcome to scb api')


@app.get("/auth/users")
async def get_users(db=Depends(get_db)):
    return crud.read_users(db)

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True) 


