from functools import wraps


def log(file_name=None):
    """Декоратор для логирования функции"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            try:
                result = func(*args,**kwargs)
                message = f'{func.__name__} ok'
                write_log(message,file_name)
                return result
            except Exception as e:
                message = f'{func.__name__} error: {type(e).__name__} inputs: {args}, {kwargs}'
                write_log(message,file_name)
                raise
        return wrapper

    return decorator

def write_log(message,file_name):
    if file_name:
        with open(file_name,'a',encoding='utf-8') as file:
            file.write(message+'\n')
    else:
        print(message)


