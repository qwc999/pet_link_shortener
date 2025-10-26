import uvicorn
from fastapi import FastAPI

from app.routers.link import link_router
from app.routers.redirect import redirect_router
from app.routers.auth import auth_router


app = FastAPI()
app.include_router(link_router, tags=["link"])
app.include_router(redirect_router)
app.include_router(auth_router, tags=["auth"])


@app.get('/')
async def main_page():
    return {"message": "main page"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
