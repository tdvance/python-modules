def switch(value, *func_args, **cases):
    """
    Usage:

    return_value = switch(value, func_arg1, func_arg2, ..., case1=func1,
    case2=func2, ..., default=func_default)

    If str(value) is casei, then funci is called on func_arg1, func_arg2,
    ..., and the result is returned.  If str(value) equals none of the
    cases, then func_default is called on func_arg1, func_arg2,
    ..., and the result is returned.

    :param value: value to compare; should be a string that is a legal
    identifier
    :param func_args: arguments to pass to the function to be called
    :param cases: The case values assigned the func names
    :return: The result of calling the chosen function
    """
    if 'default' in cases and str(value) not in cases:
        return cases['default'](*func_args)
    else:
        assert str(value) in cases, "Missing case: " + repr(str(value))
        return cases[str(value)](*func_args)
