import numexpr as ne

def calculate(expression: str):
    try:
        return str(ne.evaluate(expression))
    except Exception as e:
        return str(e)