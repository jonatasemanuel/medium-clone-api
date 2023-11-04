from fastapi import FastAPI

from api.routes import article, user, auth

app = FastAPI()

app.include_router(article.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/health-check")
def health_check():
    return True
