import uvicorn

from fastapi import FastAPI, Depends
from api.auth import crud
from api.database import engine, Base
from api.auth.router import router as auth_router
from api.testimonies.router import router as testimonies_router
from api.prayers.router import router as prayers_router


Base.metadata.create_all(bind=engine) 

app = FastAPI(title='SCB API', deescription='backend for prayer request and testimony', version='1.0.0')
app.include_router(auth_router)
app.include_router(testimonies_router)
app.include_router(prayers_router)

@app.get("/")
async def read_root():
    return ('Welcome to scb api')



if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, 
    reload=True) 


