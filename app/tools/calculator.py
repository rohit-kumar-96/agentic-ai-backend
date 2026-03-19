def calculate(expression: str):
    try:
        return str(eval(expression))
    except Exception as e:
        return str(e)