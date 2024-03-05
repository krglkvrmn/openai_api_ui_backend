from fastapi import FastAPI

from app.api.main_router import main_router
from app.auth.routers import auth_router
from app.core.config import APP_LOCAL_HOST, APP_LOCAL_PORT, OPENAPI_URL
from app.middleware import cors_middleware
from app.utils.schedulers import guests_deleter_scheduler, unverified_deleter_scheduler


app = FastAPI(openapi_url=OPENAPI_URL)
app.add_middleware(cors_middleware)

app.include_router(main_router)
app.include_router(auth_router)


@app.on_event("startup")
def startup_event():
    guests_deleter_scheduler.start()
    unverified_deleter_scheduler.start()


@app.on_event("shutdown")
def shutdown_event():
    guests_deleter_scheduler.shutdown()
    unverified_deleter_scheduler.shutdown()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=APP_LOCAL_HOST, port=APP_LOCAL_PORT)


