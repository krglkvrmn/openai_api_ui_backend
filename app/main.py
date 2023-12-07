from fastapi import FastAPI
from starlette.middleware import Middleware

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
    print('Scheduler started')
    scheduler.start()


@app.on_event("shutdown")
def shutdown_event():
    print('Scheduler shut down')
    scheduler.shutdown()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)


