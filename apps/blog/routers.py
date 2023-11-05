import time

import psycopg2
from apps.core import database, models
from fastapi import APIRouter, Depends, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from .models import Blog

router = APIRouter()

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapiblog", user="postgres", password="admin", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was OK")
        break
    except Exception as e:
        print("Database Connection Faild")
        print(e)
        time.sleep(10)


@router.get("/blogs")
def get_blogs(db: Session = Depends(database.get_db)):
    # cursor.execute("SELECT * FROM blogs")
    # blogs = cursor.fetchall()
    blogs = db.query(models.Blog).all()
    return {"data": blogs}


@router.post("/blogs", status_code=status.HTTP_201_CREATED)
def create_blog(blog: Blog, db: Session = Depends(database.get_db)):
    # cursor.execute("INSERT INTO blogs (title, content, is_published) VALUES (%s, %s, %s) RETURNING *", (blog.title, blog.content, blog.is_published))
    # new_blog = cursor.fetchone()
    # conn.commit()
    new_blog = models.Blog(title=blog.title, content=blog.content, is_published=blog.is_published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": new_blog}


@router.get("/blogs/{id}")
def get_blog(id: int):
    cursor.execute("SELECT * FROM blogs WHERE id=%s", (str(id),))
    blog = cursor.fetchone()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    return {"data": blog}


@router.delete("/blogs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int):
    cursor.execute("DELETE FROM blogs WHERE id=%s RETURNING *", (str(id),))
    deleted_blog = cursor.fetchone()
    conn.commit()
    if deleted_blog == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/blogs/{id}")
def update_post(id: int, blog: Blog):
    cursor.execute("UPDATE blogs SET title=%s, content=%s, is_published=%s WHERE id=%s RETURNING *", (blog.title, blog.content, blog.is_published, str(id)))
    updated_blog = cursor.fetchone()
    conn.commit()
    if updated_blog == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    return {"data": updated_blog}
