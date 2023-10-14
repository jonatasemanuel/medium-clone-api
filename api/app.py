from fastapi import FastAPI

from api.routes import tag

app = FastAPI()

app.include_router(tag.router)


@app.get('/health-check')
def health_check():
    return True
