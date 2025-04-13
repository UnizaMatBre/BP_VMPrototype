from source.vm_core.object_kinds import VM_ByteArray, VM_SmallInteger


def primitive_byte_array_byte_get_at(interpreter, parameters):
    byte_array_object, index_object = parameters

    assert isinstance(byte_array_object, VM_ByteArray)
    assert isinstance(index_object, VM_SmallInteger)
    assert 0 <= index_object.get_value() < byte_array_object.get_byte_count()

    return interpreter.get_universe().new_small_integer(
        byte_array_object.byte_get_at(index_object.get_value())
    )

def primitive_byte_array_byte_put_at(interpreter, parameters):
    byte_array_object, index_object, byte_object = parameters

    assert isinstance(byte_array_object, VM_ByteArray)
    assert isinstance(index_object, VM_SmallInteger)
    assert 0 <= index_object.get_value() < byte_array_object.get_byte_count()
    assert isinstance(byte_object, VM_SmallInteger)
    assert 0 <= index_object.get_value() < byte_array_object.get_byte_count()

    byte_array_object.byte_put_at(index_object.get_code(), byte_object.get_value())

    return interpreter.get_universe().get_none_object()

def primitive_byte_array_get_byte_count(interpreter, parameters):
    byte_array_object = parameters[0]

    assert isinstance(byte_array_object, VM_ByteArray)

    return interpreter.get_universe().new_small_integer(
        byte_array_object.get_byte_count()
    )


LOCAL_PRIMITIVES = (

)