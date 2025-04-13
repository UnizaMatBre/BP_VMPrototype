

def primitive_print_debug_string(interpreter, parameters):
    print("Primitive function correctly called. Debug script printed")
    print("Good job!")

    return None


LOCAL_PRIMITIVES = (
    ("printDebugString", 0, primitive_print_debug_string)
)