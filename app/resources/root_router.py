from fastapi import APIRouter

root_router = APIRouter()


@root_router.get("/")
def root():
    return {"message": "Welcome to the Composite API. See /docs for details."}



