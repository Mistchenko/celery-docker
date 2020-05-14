from decimal import Decimal
def as_decimal(val):
    try:
        res = Decimal(val)
    except:
        res = 0

    return res


def as_int(val):
    try:
        res = int(val)
    except:
        res = 0

    return res

def as_float(val):
    try:
        res = float(val)
    except:
        res = 0

    return res