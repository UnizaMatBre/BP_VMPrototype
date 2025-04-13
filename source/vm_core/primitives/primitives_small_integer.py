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

    return _do_arithmetic_operation(interpreter, left_int, right_int, lambda a,b: a+b)


def primitive_small_integer_mul(interpreter, parameters):
    left_int, right_int = parameters

    return _do_arithmetic_operation(interpreter, left_int, right_int, lambda a,b: a+b)

def primitive_small_integer_div(interpreter, parameters):
    left_int, right_int = parameters

    return _do_arithmetic_operation(interpreter, left_int, right_int, lambda a,b: a+b)

LOCAL_PRIMITIVES = (

)