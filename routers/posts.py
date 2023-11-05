import time

import psycopg2
from core import database, models
from fastapi import APIRouter, Depends, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from schemas import post
from sqlalchemy.orm import Session

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


@router.get("/posts")
def get_posts(db: Session = Depends(database.get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: post.Post, db: Session = Depends(database.get_db)):
    # cursor.execute("INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.is_published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(database.get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id=%s", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db)):
    # cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}")
def update_post(id: int, post: post.Post, db: Session = Depends(database.get_db)):
    # cursor.execute("UPDATE posts SET title=%s, content=%s, is_published=%s WHERE id=%s RETURNING *", (post.title, post.content, post.is_published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_object = post_query.first()
    if post_object == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
