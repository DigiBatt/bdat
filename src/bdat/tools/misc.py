import math
from typing import Any, Callable

import numpy as np


def make_range(args, deltaRel=(1, 1), deltaAbs=(0, 0), allowNone=False):
    for a in args:
        if a != None:
            if isinstance(a, tuple):
                return a
            else:
                return (a * deltaRel[0] + deltaAbs[0], a * deltaRel[1] + deltaAbs[1])
    if allowNone:
        return None
    raise RuntimeError("make_range: all arguments are None.")


def round_to_n(x, n):
    if x == 0:
        return x
    return round(x, -int(math.floor(math.log10(abs(x)))) + (n - 1))


def make_round_function(
    key: str, get_value: Callable[[Any, str], float]
) -> Callable[[Any], float]:
    parts = key.split(":")
    if len(parts) == 1:
        return lambda x: get_value(x, key)
    elif len(parts) == 2:
        digits = int(parts[1])
        return lambda x: round_to_n(get_value(x, parts[0]), digits)
    elif len(parts) == 3:
        key = parts[0]
        keytype = parts[1]
        value = parts[2]
        if keytype == "sig":
            return lambda x: round_to_n(get_value(x, key), int(value))
        elif keytype == "round":
            return lambda x: round(get_value(x, key), int(value))
        elif keytype == "bin":
            return lambda x: round(get_value(x, key) / float(value)) * float(value)
        elif keytype == "snap":
            v = np.array([float(x) for x in value.split(",")])
            return lambda x: v[np.argmin(np.abs(get_value(x, key) - v))]

    raise Exception("Invalid key for rounding")


def is_similar(a, b, rel_tol, abs_tol, *, exclude):
    for key in a.__dict__:
        if key in exclude:
            continue
        valueA = getattr(a, key)
        valueB = getattr(b, key)
        if valueA is None and valueB is None:
            return True
        elif isinstance(valueA, float) and isinstance(valueB, float):
            if not math.isclose(
                getattr(a, key), getattr(b, key), rel_tol=rel_tol, abs_tol=abs_tol
            ):
                return False
        else:
            return False
    return True


def make_filter(key_generator, f):
    filterspec = f.split(":")[1]
    values = []
    ranges = []
    for v in filterspec.split(","):
        if ".." in v:
            cutoffs = v.split("..")
            ranges.append((float(cutoffs[0]), float(cutoffs[1])))
        else:
            values.append(float(v))

    def filter(res):
        try:
            key_value = key_generator(res)
        except TypeError as e:
            print(e)
        return any([math.isclose(key_value, v, rel_tol=1e-4) for v in values]) or any(
            [key_value >= r[0] and key_value <= r[1] for r in ranges]
        )

    return filter


def make_getattr(key):
    def f(x):
        return getattr(x, key)

    return f
