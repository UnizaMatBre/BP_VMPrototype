
class Opcodes:

    # empty opcode, does nothing
    NOOP = 0x00

    # push running method into active frame stack
    PUSH_MYSELF = 0x10

    # push literal from specified index into active frame stack
    PUSH_LITERAL = 0x11

    # pull item from active frame stack and throw it away
    PULL = 0x1A

    # send message, selector is specified by literal index
    SEND = 0x20

    RETURN_EXPLICIT = 0x30

