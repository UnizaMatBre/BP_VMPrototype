

def primitive_debug_print_special_string(interpreter, parameters):
    print("Primitive function correctly called. Debug script printed")
    print("Good job!")

    return None


LOCAL_PRIMITIVES = (
    ("debug_printSpecialString", 0, primitive_debug_print_special_string)
)