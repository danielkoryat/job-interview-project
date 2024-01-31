
def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"error in {func.__name__}: {e}", flush=True)
    return wrapper