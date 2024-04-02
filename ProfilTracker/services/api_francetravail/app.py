from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from common.log_config import setup_logging
from api_francetravail.auth.auth import FranceTravailAuth
from api_francetravail.api import FranceTravailAPI
import os

load_dotenv()

logger = setup_logging(os.getenv("SERVICE_NAME"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    authen = FranceTravailAuth()
    app.state.api_service = FranceTravailAPI(auth=authen)
    try:
        yield
    finally:
        logger.info("Application shutdown")


app = FastAPI(lifespan=lifespan)


@app.get("/status")
async def get_status():
    try:
        return await app.state.api_service.get_status()
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred"
        )


@app.get("/data")
async def get_data():
    try:
        return await app.state.api_service.get_data()
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred"
        )


@app.get("/info")
def get_info():
    return app.state.api_service.get_info()
