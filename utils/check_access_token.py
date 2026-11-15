from functools import wraps
from .auth import Auth


def with_fresh_token(auth: Auth):
    """Перед вызовом функции проверяет токен и обновляет его, если он просрочен."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if auth.is_expired():
                auth.update()
            return func(*args, **kwargs)
        return wrapper
    return decorator