from fastapi import FastAPI, HTTPException, Response, APIRouter
import os

router = APIRouter()

@router.get("/")
def read_root() -> Response:
    return Response("The server is running!!")


