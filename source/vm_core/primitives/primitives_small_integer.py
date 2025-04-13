from source.vm_core.object_kinds import VM_SmallInteger


def primitive_small_integer_add(interpreter, parameters):
    left_int, right_int = parameters

    assert isinstance(left_int, VM_SmallInteger)
    assert isinstance(right_int, VM_SmallInteger)

    return interpreter.get_universe().new_small_integer(
        left_int.get_value() + right_int.get_value()
    )


def primitive_small_integer_sub(interpreter, parameters):
    left_int, right_int = parameters

    assert isinstance(left_int, VM_SmallInteger)
    assert isinstance(right_int, VM_SmallInteger)

    return interpreter.get_universe().new_small_integer(
        left_int.get_value() - right_int.get_value()
    )


def primitive_small_integer_mul(interpreter, parameters):
    left_int, right_int = parameters

    assert isinstance(left_int, VM_SmallInteger)
    assert isinstance(right_int, VM_SmallInteger)

    return interpreter.get_universe().new_small_integer(
        left_int.get_value() * right_int.get_value()
    )

def primitive_small_integer_div(interpreter, parameters):
    left_int, right_int = parameters

    assert isinstance(left_int, VM_SmallInteger)
    assert isinstance(right_int, VM_SmallInteger)

    return interpreter.get_universe().new_small_integer(
        int(left_int.get_value() / right_int.get_value())
    )

LOCAL_PRIMITIVES = (

)