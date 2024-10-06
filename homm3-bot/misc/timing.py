from time import time
from functools import wraps

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print (f"{f}: time: {te-ts}")
        return result
    return wrap
