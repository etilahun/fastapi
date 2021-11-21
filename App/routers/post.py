
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from fastapi import Response, status, HTTPException, APIRouter 
from typing import List, Optional
from .. import schemas, oauth2
from ..database import conn, cur

router = APIRouter(
  prefix="/posts",
  tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(response: Response, limit: int = 10, skip: int = 0, search: Optional[str] = ''):

  search =  '%' + search + '%'
  cur.execute("""SELECT * FROM posts WHERE title LIKE %s LIMIT %s OFFSET %s""", (search, str(limit), str(skip))) 
  posts = cur.fetchall()
  # print(posts)
  return posts


@router.get("/{withcount}", response_model=List[schemas.PostCountResponse])
def get_posts_count(response: Response): 

  cur.execute("""SELECT p.*, COUNT(v.post_id) AS votes FROM posts p LEFT JOIN votes v ON p.id = v.post_id GROUP BY p.id""") 

  posts = cur.fetchall()
  # print(posts)
  return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, current_user = Depends(oauth2.get_current_user)): 
  print(current_user)
  print(type(current_user))

  cur.execute("""INSERT INTO posts (title, content, published, user_id) VALUES (%s, %s, %s, %s) RETURNING *""", (post.title, post.content, post.published, current_user['id']))

  new_post = cur.fetchone()
  conn.commit()

  return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, response: Response): 

  cur.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),)) 
  post = cur.fetchone()
  if not post:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail=f"post with id: {id} was not found"
    )
  return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, current_user = Depends(oauth2.get_current_user)):

  cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),)) 
  
  deleted_post = cur.fetchone()

  if deleted_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

  if deleted_post['user_id'] != current_user['id']:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

  conn.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)  


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, current_user: int = Depends(oauth2.get_current_user)): 

  cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),)) 

  updated_post = cur.fetchone()
  
  if updated_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

  if updated_post['user_id'] != current_user['id']:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

  conn.commit()

  return updated_post