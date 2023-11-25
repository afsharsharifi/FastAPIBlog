from core import database, models
from fastapi import FastAPI
from routers import posts, users, auth, votes
from core.config import settings

# models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "This is Root"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(votes.router)
