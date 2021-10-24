from fastapi import FastAPI
from pipeline import run_pipeline

app = FastAPI()


@app.get("/")
async def root():
    import os
    print(os.environ)
    run_pipeline()
    return {'Message': 'finished'}
