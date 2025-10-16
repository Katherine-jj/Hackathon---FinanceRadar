import uuid
def make_correlation_id():
    return uuid.uuid4().hex
