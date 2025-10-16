from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api import transactions
from app.db import models
from app.db.session import engine
from app.logging_config import setup_logging
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils import make_correlation_id
import logging
import os

setup_logging()
logger = logging.getLogger("fraud")

models.Base.metadata.create_all(bind=engine)  # for dev; use Alembic for prod

app = FastAPI(title="Fraud Panel")

app.include_router(transactions.router, prefix="/api")

templates = Jinja2Templates(directory="app/templates")

# correlation id middleware
class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        corr = request.headers.get("X-Correlation-ID") or make_correlation_id()
        request.state.correlation_id = corr
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = corr
        logger.info("req", extra={"correlation_id": corr, "path": str(request.url.path)})
        return response

app.add_middleware(CorrelationMiddleware)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("admin_rules.html", {"request": request})
