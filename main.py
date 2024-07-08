from fastapi import FastAPI
import uvicorn
from api import models
from api.postgresql.db import engine
from fastapi.middleware.cors import CORSMiddleware

from api.users.auth_routes import router as auth_router
from api.posts.post_routes import router as posts_router
from api.votes.vote_routes import router as votes_router
from api.tags.tag_routes import router as tags_router
from api.comments.comment_routes import router as comment_router
from api.unauthorized_routes import router as unauthorized_router


app = FastAPI(
    title="API"
)
origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

models.Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(votes_router)
app.include_router(tags_router)
app.include_router(comment_router)
app.include_router(unauthorized_router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
