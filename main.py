from fastapi import Request, FastAPI

from src.auth.router import router as auth_router
from src.database import init_db

init_db()

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
async def auth_page(request: Request):
    return {"message": "go to /docs for view swagger ui"}