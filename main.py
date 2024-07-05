from fastapi import FastAPI
import uvicorn
from api import models
from api.postgresql.db import engine

from api.users.auth_routes import router as auth_router
from api.posts.post_routes import router as posts_router
from api.comments.comment_routes import router as comment_router

app = FastAPI(
    title="API"
)

models.Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(comment_router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
