from fastapi import Response, status, HTTPException, APIRouter 
from .. import schemas, utils 
from ..database import conn, cur 

router = APIRouter(
  prefix="/users", 
  tags=['Users'] 
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate): 
  hashed_password = utils.hash(user.password)
  user.password = hashed_password

  cur.execute("""INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id, email, created_at""", (user.email, user.password))
  new_user = cur.fetchone()
  conn.commit()

  return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_post(id: int, response: Response): 

  cur.execute("""SELECT * FROM users WHERE id = %s""", (str(id),)) 
  user = cur.fetchone()
  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail=f"user with id: {id} was not found"
    )
    
  return user