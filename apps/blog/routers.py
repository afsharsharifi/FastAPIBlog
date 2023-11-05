import time

import psycopg2
from apps.core import database, models
from fastapi import APIRouter, Depends, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from .schemas import Blog

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
    new_blog = models.Blog(**blog.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": new_blog}


@router.get("/blogs/{id}")
def get_blog(id: int, db: Session = Depends(database.get_db)):
    # cursor.execute("SELECT * FROM blogs WHERE id=%s", (str(id),))
    # blog = cursor.fetchone()
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    return {"data": blog}


@router.delete("/blogs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(database.get_db)):
    # cursor.execute("DELETE FROM blogs WHERE id=%s RETURNING *", (str(id),))
    # deleted_blog = cursor.fetchone()
    # conn.commit()
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if blog.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    blog.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/blogs/{id}")
def update_post(id: int, blog: Blog, db: Session = Depends(database.get_db)):
    # cursor.execute("UPDATE blogs SET title=%s, content=%s, is_published=%s WHERE id=%s RETURNING *", (blog.title, blog.content, blog.is_published, str(id)))
    # updated_blog = cursor.fetchone()
    # conn.commit()
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    blog_object = blog_query.first()
    if blog_object == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    blog_query.update(blog.model_dump(), synchronize_session=False)
    db.commit()
    return {"data": blog_query.first()}
