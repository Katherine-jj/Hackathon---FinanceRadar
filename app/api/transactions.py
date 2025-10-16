from fastapi import APIRouter, Depends, Request, BackgroundTasks
from app.schemas import TransactionIn
from app.utils import make_correlation_id
from app.db.session import SessionLocal
from app.db import models
from redis import Redis
from rq import Queue
import os
import json

router = APIRouter()
redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_conn = Redis.from_url(redis_url)
q = Queue("transactions", connection=redis_conn, default_timeout=120)

def enqueue_tx_job(correlation_id, payload):
    # pushes to redis queue; worker will process
    q.enqueue("app.workers.worker.process_transaction", correlation_id, payload)

@router.post("/transactions")
async def post_transaction(tx: TransactionIn, request: Request):
    correlation_id = make_correlation_id()
    payload = tx.dict()
    payload["correlation_id"] = correlation_id

    # quick persist minimal log record
    db = SessionLocal()
    log = models.TransactionLog(correlation_id=correlation_id, payload=payload)
    db.add(log); db.commit(); db.close()

    enqueue_tx_job(correlation_id, payload)
    return {"status":"accepted", "correlation_id": correlation_id}
