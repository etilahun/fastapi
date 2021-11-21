from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, utils, oauth2, database

router = APIRouter(tags=['Authentication'])

@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()): 

  cur = database.cur
  cur.execute("""SELECT * FROM users WHERE email = %s""", (user_credentials.username,))
  
  user = cur.fetchone()

  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

  if not utils.verify(user_credentials.password, user['password']):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

  access_token = oauth2.create_access_token(data={"user_id": user['id']})

  return {"access_token": access_token, "token_type": "bearer"}
