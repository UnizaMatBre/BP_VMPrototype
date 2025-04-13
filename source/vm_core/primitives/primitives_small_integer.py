from source.vm_core.object_kinds import VM_SmallInteger


def _do_arithmetic_operation(interpreter, left_int, right_int, operation):
    assert isinstance(left_int, VM_SmallInteger)
    assert isinstance(right_int, VM_SmallInteger)

    return interpreter.get_universe().new_small_integer(
        operation(
            left_int.get_code(),
            right_int.get_value()
        )
    )

def primitive_small_integer_add(interpreter, parameters):
    left_int, right_int = parameters

    return _do_arithmetic_operation(interpreter, left_int, right_int, lambda a,b: a+b)


def primitive_small_integer_sub(interpreter, parameters):
    left_int, right_int = parameters

    return _do_arithmetic_operation(interpreter, left_int, right_int, lambda a,b: a-b)


def primitive_small_integer_mul(interpreter, parameters):
    left_int, right_int = parameters

    return _do_arithmetic_operation(interpreter, left_int, right_int, lambda a,b: a*b)

def primitive_small_integer_div(interpreter, parameters):
    left_int, right_int = parameters

    return _do_arithmetic_operation(interpreter, left_int, right_int, lambda a,b: int(a/b))


def _do_comparison_operation(interpreter, left_int, right_int, predicate):
    assert isinstance(left_int, VM_SmallInteger)
    assert isinstance(right_int, VM_SmallInteger)

    result = predicate(left_int.get_value(), right_int.get_value())

    if result:
        return interpreter.get_universe().get_true_object()
    else:
        return interpreter.get_universe().get_false_object()

def primitive_small_integer_equal(interpreter, parameters):
    left_int, right_int = parameters

    return _do_comparison_operation(interpreter, left_int, right_int, lambda a,b: a==b)

def primitive_small_integer_greater(interpreter, parameters):
    left_int, right_int = parameters

    return _do_comparison_operation(interpreter, left_int, right_int, lambda a,b: a>b)

def primitive_small_integer_lesser(interpreter, parameters):
    left_int, right_int = parameters

    return _do_comparison_operation(interpreter, left_int, right_int, lambda a,b: a<b)


def primitive_small_integer_as_string(interpreter, parameters):
    integer = parameters[0]

    assert isinstance(integer, VM_SmallInteger)

    return interpreter.get_universe().new_string(
        str(integer.get_value()).encode("utf-8")
    )


LOCAL_PRIMITIVES = (

)