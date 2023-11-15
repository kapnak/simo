from decimal import Decimal
import decimal

ctx = decimal.Context()
ctx.prec = 9


def add(a, b):
    return float(Decimal(str(a)) + Decimal(str(b)))


def substract(a, b):
    return float(Decimal(str(a)) - Decimal(str(b)))


def multiply(a, b):
    return float(Decimal(str(a)) * Decimal(str(b)))


def divide(a, b):
    return float(Decimal(str(a)) / Decimal(str(b)))


def float_to_str(f):
    """
    Convert the given float to a string,
    without resorting to scientific notation
    """
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')
