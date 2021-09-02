
from fastapi import FastAPI, Depends, HTTPException

from routers.user_router import router as router_user

from fastapi.middleware.cors import CORSMiddleware

api = FastAPI() 

origins = [
"http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
"http://localhost", "http://localhost:8080"
] 
api.add_middleware(
CORSMiddleware, allow_origins=origins,
allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
) 

api.include_router(router_user)