from fastapi import FastAPI
from apps.blog import routers as BlogRoutes

app = FastAPI()


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "This is Root"}


app.include_router(BlogRoutes.router, tags=["Blog"])
