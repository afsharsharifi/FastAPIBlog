from fastapi import APIRouter
from .models import Blog


router = APIRouter()


my_posts = [
    {
        "id": 1,
        "title": "This is 1 title",
        "content": "Here",
    },
    {
        "id": 2,
        "title": "This is 2 title",
        "content": "Here",
    },
    {
        "id": 3,
        "title": "This is 3 title",
        "content": "Here",
    },
    {
        "id": 4,
        "title": "This is 4 title",
        "content": "Here",
    },
]


@router.get("/blog")
def get_blogs():
    return {"data": my_posts}


@router.post("/blog")
def create_blogs(blog: Blog):
    new_id = my_posts[-1]["id"] + 1
    post_dict = blog.model_dump()
    post_dict["id"] = new_id
    my_posts.append(post_dict)
    return {"data": post_dict}
