from fastapi import APIRouter, HTTPException, Response, status

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


def find_blog_index_by_id(id: int):
    for index, blog in enumerate(my_blogs):
        if blog["id"] == id:
            return index


@router.get("/blogs")
def get_blogs():
    return {"data": my_blogs}


@router.post("/blogs", status_code=status.HTTP_201_CREATED)
def create_blog(blog: Blog):
    new_id = my_blogs[-1]["id"] + 1
    post_dict = blog.model_dump()
    post_dict["id"] = new_id
    my_blogs.append(post_dict)
    return {"data": post_dict}


@router.get("/blogs/{id}")
def get_blog(id: int):
    blog = find_blog_by_id(id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    return {"data": blog}


@router.delete("/blogs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int):
    blog_index = find_blog_index_by_id(id)
    if blog_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    my_blogs.pop(blog_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/blogs/{id}")
def update_post(id: int, blog: Blog):
    blog_index = find_blog_index_by_id(id)
    if blog_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    blog_dict = blog.model_dump()
    blog_dict["id"] = id
    my_blogs[blog_index] = blog_dict
    return {"data": blog_dict}
