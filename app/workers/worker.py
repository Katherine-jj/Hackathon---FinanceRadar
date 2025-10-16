# worker entrypoint used by rq: the function referenced above lives in this module
import os
import time
from app.db.session import SessionLocal
from app.db.models import Rule, TransactionLog
from app.rules.engine import RuleEngine
from app.notifications import send_alert_webhook
import json

def load_rules(db):
    return db.query(Rule).filter(Rule.enabled==True).all()

def process_transaction(correlation_id, payload):
    db = SessionLocal()
    try:
        rules = load_rules(db)
        engine = RuleEngine(rules)
        alerted, reason = engine.apply(payload)
        # update log
        log = db.query(TransactionLog).filter_by(correlation_id=correlation_id).one_or_none()
        if log:
            log.alerted = alerted
            log.alert_reason = reason
            db.add(log)
            db.commit()
        if alerted:
            send_alert_webhook({"correlation_id": correlation_id, "payload": payload, "reason": reason})
    finally:
        db.close()

if __name__ == "__main__":
    # This block runs if the worker container is started directly (development)
    print("Worker ready (this script is used by RQ).")
    while True:
        time.sleep(3600)
