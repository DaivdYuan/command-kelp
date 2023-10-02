from functools import wraps
import os, json

DEVNULL = open(os.devnull, 'w')

def sanitize_one_line(text):
    # get only the first line, and strip the newline character
    return text.split("\n")[0].strip()

def memoize(fn):
    """Caches previous calls to the function."""
    memo = {}

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not memoize.disabled:
            key = json.dumps((args, kwargs))
            if key not in memo:
                memo[key] = fn(*args, **kwargs)
            value = memo[key]
        else:
            # Memoize is disabled, call the function
            value = fn(*args, **kwargs)

        return value

    return wrapper