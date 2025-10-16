from pydantic import BaseModel
from typing import Any, Dict, Optional

class TransactionIn(BaseModel):
    amount: float
    from_account: str
    to_account: str
    ts: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class RuleCreate(BaseModel):
    name: str
    type: str
    params: Dict[str, Any]
    enabled: bool = True
