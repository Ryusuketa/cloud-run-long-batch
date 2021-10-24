from fastapi import FastAPI
from pipeline import run_pipeline

app = FastAPI()


@app.get("/")
async def root():
    run_pipeline()
    return {'Message': 'finished'}
