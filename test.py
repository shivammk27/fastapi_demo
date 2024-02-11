from typing import Annotated, get_type_hints, get_origin, get_args
from functools import wraps

def check_value_range(func):
    @wraps(func)
    def wrapped(x):
        # type_hints = get_type_hints(double) # o/p = {'x': <class 'int'>, 'return': <class 'int'>}
        # o/p = {'x': typing.Annotated[int, (0, 100)], 'return': <class 'int'>}
        type_hints = get_type_hints(double, include_extras=True)
        # print(type_hints)
        hint = type_hints['x']  # o/p = typing.Annotated[int, (0, 100)]
        if get_origin(hint) is Annotated:
            hint_type, *hint_args = get_args(hint)
            # print(hint_type)    # o/p = <class, 'int'>
            # print(hint_args)    # o/p = [(0, 100)]
            low, high = hint_args[0]  # o/p = 0, 100
            # print(low, high)
            if not low <= x <= high:
                raise ValueError(f"{x} falls outside boundary {low}-{high}")

        # execute function once all checks passed
        return func(x)
    return wrapped


@check_value_range
def double(x: Annotated[int, (0, 100)]) -> int:
    return x*2


result = double(10)
print(result)
