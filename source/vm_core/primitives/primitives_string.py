from source.vm_core.object_kinds import VM_ByteArray, VM_SmallInteger, VM_String


def primitive_string_character_get_at(interpreter, parameters):
    string_object, index_object = parameters

    assert isinstance(string_object, VM_String)
    assert isinstance(index_object, VM_SmallInteger)
    assert 0 <= index_object.get_value() < string_object.get_character_count()

    return interpreter.get_universe().new_small_integer(
        string_object.character_get_at(index_object.get_value())
    )

def primitive_string_get_character_count(interpreter, parameters):
    string_object = parameters[0]

    assert isinstance(string_object, VM_String)

    return interpreter.get_universe().new_small_integer(
        string_object.get_character_count()
    )

def primitive_string_as_symbol(interpreter, parameters):
    string_object, arity_object = parameters

    assert isinstance(string_object, VM_String)
    assert isinstance(arity_object, VM_SmallInteger)
    assert arity_object.get_value() >= 0

    return interpreter.get_universe().new_symbol(
        string_object.get_characters().encode(encoding="ascii"), arity_object.get_value()
    )


LOCAL_PRIMITIVES = (

)