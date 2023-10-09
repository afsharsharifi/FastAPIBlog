from fastapi import APIRouter
from .models import Blog


router = APIRouter()


my_blogs = [
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


def find_blog_by_id(id: int):
    for blog in my_blogs:
        if blog["id"] == id:
            return blog


@router.get("/blogs")
def get_blogs():
    return {"data": my_blogs}


@router.post("/blogs")
def create_blog(blog: Blog):
    new_id = my_blogs[-1]["id"] + 1
    post_dict = blog.model_dump()
    post_dict["id"] = new_id
    my_blogs.append(post_dict)
    return {"data": post_dict}


@router.get("/blogs/{id}")
def get_blog(id: int):
    blog = find_blog_by_id(id)
    return {"data": blog}
