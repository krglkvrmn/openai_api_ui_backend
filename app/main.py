from fastapi import FastAPI

from app.api.main_router import main_router
from app.auth.routers import fastapi_users, auth_router
from app.middleware import cors_middleware
from app.utils.schedulers import scheduler

app = FastAPI()
app.add_middleware(cors_middleware)

app.include_router(main_router)
app.include_router(auth_router)


@app.on_event("startup")
def startup_event():
    scheduler.start()


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)


