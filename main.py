from core import database, models
from fastapi import FastAPI
from routers import posts as PostRoutes
from routers import users as UserRoutes

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "This is Root"}


app.include_router(PostRoutes.router, tags=["Posts"])
app.include_router(UserRoutes.router, tags=["Users"])
