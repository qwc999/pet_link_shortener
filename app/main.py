from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.redis_cache import redis_cache
from app.routers.admin import admin_router
from app.routers.link import link_router
from app.routers.redirect import redirect_router
from app.routers.auth import auth_router
from app.routers.user import user_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await redis_cache.init_redis()
    yield
    await redis_cache.close_redis()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, tags=["user"])
app.include_router(link_router, tags=["link"])
app.include_router(admin_router, tags=["admin"])
app.include_router(redirect_router)


@app.get('/')
async def main_page():
    return {"message": "main page"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
