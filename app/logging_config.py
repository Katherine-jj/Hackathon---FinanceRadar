import logging, sys, jsonlog_formatter

def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlog_formatter.JSONFormatter(fmt="%(message)s")
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)
