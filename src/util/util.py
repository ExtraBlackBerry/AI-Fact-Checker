import inspect

def error_code(code=6, message="Unknown error"):

        func_name = inspect.stack()[1].function

        return  {
        "error_code": code,
        "message": message,
        "origin": func_name
    }

def result(data = None):
        func_name = inspect.stack()[1].function

        if not data:
            return {
                "error_code": 404,
                "message": "Return Value is empty",
                "origin": func_name
                }

        return  {
        "error_code": 0,
        "message": data,
        "origin": func_name
    }

def print_error(error):
       print(f"error code: {error['error_code']}, message: {error['message']}, source: {error['origin']} ")