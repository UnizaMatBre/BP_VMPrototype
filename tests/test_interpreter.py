from source.vm_core import object_kinds
from source.vm_core.interpreter import Interpreter
from source.vm_core.instructions import Opcodes

from collections import namedtuple
import unittest

from source.vm_core.object_kinds import VM_ByteArray, VM_ObjectArray

SetupResult = namedtuple("SetupResult", ("literals", "bytecode", "stack", "frame"))


class InstructionsTestCase(unittest.TestCase):
    def _setup_process(self, literals_content, bytecode_content, stack_content, none_object):
        bytecode = VM_ByteArray(len(bytecode_content))
        for index in range(len(bytecode_content)):
            bytecode.byte_put_at(index, bytecode_content[index])

        literals = VM_ObjectArray(len(literals_content), none_object)
        for index in range(len(literals_content)):
            literals.item_put_at(index, literals_content[index])

        stack = VM_ObjectArray(len(stack_content), none_object)
        for index in range(len(stack_content)):
            stack.item_put_at(index, stack_content[index])

        method = object_kinds.VM_Method(literals, bytecode)
        frame = object_kinds.VM_Frame(none_object, stack, method)

        return SetupResult(
            literals=literals,
            bytecode=bytecode,
            stack=stack,
            frame=frame
        )



    def test_nothing_opcode(self):
        # setup
        setup = self._setup_process(
            literals_content=[None],
            stack_content=[None],
            bytecode_content=[Opcodes.NOOP, 0x00],
            none_object=None
        )

        # testing
        process = object_kinds.VM_Proces(setup.frame)
        interpreter = Interpreter(process)
        interpreter.executeInstruction()

        self.assertTrue(
            all( (setup.stack.item_get_at(index) is None) for index in range(setup.stack.get_item_count()) ),
            "When noop opcode is executed, stack must be in its original state"
        )

    def test_push_myself_opcode(self):
        # setup
        setup = self._setup_process(
            literals_content=[None],
            stack_content=[None],
            bytecode_content=[Opcodes.PUSH_MYSELF, 0x00],
            none_object=None
        )

        # testing
        process = object_kinds.VM_Proces(setup.frame)
        interpreter = Interpreter(process)
        interpreter.executeInstruction()

        self.assertTrue(
            setup.stack.item_get_at(0) is process.peek_frame().getMethodActivation(),
            "When push_myself opcode is executed, top of the stack must be running method"
        )

        self.assertTrue(
            all((setup.stack.item_get_at(index) is None) for index in range(setup.stack.get_item_count())),
            "When push_myself opcode is executed, rest of the stack must be in original state"
        )

    def test_push_literal_opcode(self):
        # setup
        setup = self._setup_process(
            literals_content=[object_kinds.VM_Symbol("to_be_cloned", 0)],
            stack_content=[None] * 4,
            bytecode_content=[Opcodes.PUSH_LITERAL, 0x00],
            none_object=None
        )

        # testing
        process = object_kinds.VM_Proces(setup.frame)
        interpreter = Interpreter(process)
        interpreter.executeInstruction()

        self.assertTrue(
            setup.stack.item_get_at(0) == setup.literals.item_get_at(0),
            "When push_literal opcode is executed, top of the stack should be copy of literal referenced by it"
        )

        self.assertTrue(
            all((setup.stack.item_get_at(index) is None) for index in range(setup.stack.get_item_count())),
            "When push_literal opcode is executed, rest of the stack must be in original state"
        )

if __name__ == '__main__':
    unittest.main()