# simple pluggable rule engine
from typing import Dict, Any, List
from app.db.models import Rule
import re

class RuleEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = [r for r in rules if r.enabled]

    def apply(self, tx: Dict[str, Any]):
        """Return (alerted: bool, reason: str|None)"""
        for r in self.rules:
            if r.type == "threshold":
                # params: {"field":"amount","op":">","value":1000}
                f = r.params.get("field")
                op = r.params.get("op")
                val = r.params.get("value")
                tx_val = tx.get(f)
                if tx_val is None:
                    continue
                if op == ">" and float(tx_val) > float(val):
                    return True, f"rule:{r.name} threshold {f} {op} {val}"
                if op == "<" and float(tx_val) < float(val):
                    return True, f"rule:{r.name} threshold {f} {op} {val}"
            elif r.type == "pattern":
                # params: {"field":"to_account","pattern":"^VIP.*"}
                f = r.params.get("field")
                pattern = r.params.get("pattern")
                tx_val = str(tx.get(f,""))
                if re.search(pattern, tx_val):
                    return True, f"rule:{r.name} pattern matched {pattern}"
            elif r.type == "composite":
                # params: {"expr": "amount>1000 and to_account.startswith('X')"}
                # naive (dangerous) eval — replace with safe evaluator in prod
                expr = r.params.get("expr")
                try:
                    allowed = {"__builtins__":{}}
                    # prepare local mapping
                    locals_map = {k: v for k,v in tx.items()}
                    if eval(expr, allowed, locals_map):
                        return True, f"rule:{r.name} composite {expr}"
                except Exception:
                    continue
        return False, None
