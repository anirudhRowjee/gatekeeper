# helpers module
# 1. Passcode Generator
import uuid

def gen_UID():
    return str(uuid.uuid4()).split('-')[-1]
