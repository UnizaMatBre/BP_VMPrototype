from source.vm_core import object_kinds
from source.vm_core.interpreter import Interpreter
from source.vm_core.instructions import Opcodes


import unittest

class InstructionsTestCase(unittest.TestCase):


    def test_nothing_opcode(self):
        # setup
        bytecode = object_kinds.VM_ByteArray(2)
        bytecode.byte_put_at(0, Opcodes.NOOP)
        bytecode.byte_put_at(1, 0x00)

        literals = object_kinds.VM_ObjectArray(0, None)

        method = object_kinds.VM_Method(literals, bytecode)

        stack = object_kinds.VM_ObjectArray(10, None)

        frame = object_kinds.VM_Frame(None, stack, method)

        process = object_kinds.VM_Proces(frame)

        # testing
        interpreter = Interpreter(process)
        interpreter.executeInstruction()

        self.assertTrue(
            all( (stack.item_get_at(index) is None) for index in range(stack.get_item_count()) ),
            "When noop opcode is executed, stack must be in its original state"
        )




if __name__ == '__main__':
    unittest.main()