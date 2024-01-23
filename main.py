import uvicorn

from fastapi import FastAPI


app = FastAPI(title='SCB API', deescription='backend for prayer request and testimony', version='1.0.0')

@app.get("/")
async def read_root():
    return ('Welcome to scb api')

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True) 


