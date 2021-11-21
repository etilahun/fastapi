from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote
from .config import settings

print(settings.db_username)

app = FastAPI()

origins = ['http://www.google.com', 'http://www.youtube.com', 'http://www.ebay.com'] 
app.add_middleware(
  CORSMiddleware, 
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"], 
  allow_headers=["*"]
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():  # async def root():  
  # return {"message": "Hello World"}
  return {"message": "Welcome to my API"} 
