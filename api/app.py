from fastapi import FastAPI

from api.routes import tag, article

app = FastAPI()

app.include_router(tag.router)
app.include_router(article.router)


@app.get("/health-check")
def health_check():
    return True
