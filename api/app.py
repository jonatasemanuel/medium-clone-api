from fastapi import FastAPI

from api.routes import article, comments, favorites, profile, tags, user

app = FastAPI()

app.include_router(article.router)
app.include_router(comments.router)
app.include_router(user.router)
app.include_router(profile.router)
app.include_router(favorites.router)
app.include_router(tags.router)


@app.get('/health-check')
def health_check():
    return True
