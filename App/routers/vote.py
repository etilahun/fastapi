
from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, database, oauth2


router = APIRouter(
  prefix="/vote",
  tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, current_user: int = Depends(oauth2.get_current_user)):

  conn = database.conn
  cur = database.cur

  cur.execute("""SELECT * FROM posts WHERE id = %s""", ( vote.post_id,)) 
  post = cur.fetchone()

  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

  cur.execute("""SELECT * FROM votes WHERE user_id = %s AND post_id = %s""", (current_user['id'], vote.post_id)) 
  found_vote = cur.fetchone()

  if (vote.dir == 1):
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user['id']} has already voted on post {vote.post_id}")

    cur.execute("""INSERT INTO votes (user_id, post_id) VALUES (%s, %s) RETURNING *""", (current_user['id'], vote.post_id)) 
    new_vote = cur.fetchone()

    conn.commit()

    return {"message": "Successfully added vote"}
  else:
    if not found_vote:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

    cur.execute("""DELETE FROM votes WHERE user_id = %s AND post_id = %s RETURNING *""", (current_user['id'], vote.post_id)) 
    deleted_vote = cur.fetchone()

    conn.commit()

    return {"message": "Successfully deleted vote"}