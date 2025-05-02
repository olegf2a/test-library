import uvicorn
from fastapi import FastAPI

from app.api.routers.books import router as users_router

app = FastAPI(title="Library", docs_url="/api/docs")

app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
