from source.vm_core import object_kinds
from source.vm_core.interpreter import Interpreter
from source.vm_core.instructions import Opcodes

from collections import namedtuple
import unittest

from source.vm_core.object_kinds import VM_ByteArray, VM_ObjectArray
from source.vm_core.object_layout import SlotKind

SetupResult = namedtuple("SetupResult", ("literals", "bytecode", "stack", "frame"))


class UniverseMockup:
    def get_none_object(self):
        return None

    def new_frame_with_stack_size(self, stack_size, method_activation):
        stack = object_kinds.VM_ObjectArray(stack_size, self.get_none_object())
        frame = object_kinds.VM_Frame(self.get_none_object(), stack, method_activation)

        return frame

def _setup_process(literals_content, bytecode_content, stack_content, none_object):
    bytecode = VM_ByteArray(len(bytecode_content))
    for index in range(len(bytecode_content)):
        bytecode.byte_put_at(index, bytecode_content[index])

    literals = VM_ObjectArray(len(literals_content), none_object)
    for index in range(len(literals_content)):
        literals.item_put_at(index, literals_content[index])

    stack = VM_ObjectArray(len(stack_content), none_object)
    code = object_kinds.VM_Code(literals, bytecode)

    method = object_kinds.VM_Object()
    method.set_code(code)

    frame = object_kinds.VM_Frame(none_object, stack, method)

    for index in range(len(stack_content)):
        if stack_content[index] is none_object:
            break
        frame.push_item(stack_content[index])

    return SetupResult(
        literals=literals,
        bytecode=bytecode,
        stack=stack,
        frame=frame
    )

class InstructionNothingTestCase(unittest.TestCase):
    def test_nothing_opcode_correct(self):
        # setup
        setup = _setup_process(
            literals_content=[None],
            stack_content=[None],
            bytecode_content=[Opcodes.NOOP, 0x00],
            none_object=None
        )

        # testing
        process = object_kinds.VM_Process(None, setup.frame)
        interpreter = Interpreter(UniverseMockup(), process)
        interpreter.executeInstruction()

        self.assertTrue(
            all( (setup.stack.item_get_at(index) is None) for index in range(setup.stack.get_item_count()) ),
            "When noop opcode is executed, stack must be in its original state"
        )

class InstructionPushMyselfTestCase(unittest.TestCase):
    def test_push_myself_opcode(self):
        # setup
        setup = _setup_process(
            literals_content=[None],
            stack_content=[None],
            bytecode_content=[Opcodes.PUSH_MYSELF, 0x00],
            none_object=None
        )

        # testing
        process = object_kinds.VM_Process(None, setup.frame)
        interpreter = Interpreter(UniverseMockup(), process)
        interpreter.executeInstruction()

        self.assertTrue(
            setup.stack.item_get_at(0) is process.peek_frame().get_method_activation(),
            "When push_myself opcode is executed, top of the stack must be running method"
        )

class InstructionPushLiteralTestCase(unittest.TestCase):
    def test_push_literal_opcode_correct(self):
        # setup
        setup = _setup_process(
            literals_content=[object_kinds.VM_Symbol("to_be_cloned", 0)],
            stack_content=[None] * 4,
            bytecode_content=[Opcodes.PUSH_LITERAL, 0x00],
            none_object=None
        )

        # testing
        process = object_kinds.VM_Process(None, setup.frame)
        interpreter = Interpreter(UniverseMockup(), process)
        interpreter.executeInstruction()

        self.assertTrue(
            setup.stack.item_get_at(0) == setup.literals.item_get_at(0),
            "When push_literal opcode is executed, top of the stack should be copy of literal referenced by it"
        )

class InstructionPullTestCase(unittest.TestCase):
    def test_pull_opcode_correct(self):
        pulled_object =  object_kinds.VM_Symbol("to_be_returned", 0)

        setup = _setup_process(
            literals_content=[],
            stack_content=[pulled_object],
            bytecode_content=[Opcodes.PULL, 0x00],
            none_object=None
        )

        process = object_kinds.VM_Process(None, setup.frame)
        interpreter = Interpreter(UniverseMockup(), process)
        interpreter.executeInstruction()

        self.assertTrue(
            setup.stack.item_get_at(0) is None and setup.frame.is_stack_empty(),
            "When pull opcode is executed, stack should be empty"
        )

class InstructionReturnExplicitTestCase(unittest.TestCase):
    def test_return_explicit_opcode_correct(self):
        # setup for root frame
        returned_object = object_kinds.VM_Symbol("to_be_returned", 0)

        setup_for_root_frame = _setup_process(
            literals_content=[],
            stack_content=[None] * 4,
            bytecode_content=[],
            none_object=None
        )

        # setup for sub method
        setup_for_sub_frame = _setup_process(
            literals_content=[],
            stack_content=[returned_object, None],
            bytecode_content=[Opcodes.RETURN_EXPLICIT, 0x00],
            none_object=None
        )

        # testing
        process = object_kinds.VM_Process(None, setup_for_root_frame.frame)
        process.push_frame(setup_for_sub_frame.frame)

        interpreter = Interpreter(UniverseMockup(), process)
        interpreter.executeInstruction()

        self.assertTrue(
            process.peek_frame() is setup_for_root_frame.frame,
            "When return_explicit opcode is executed, the active frame must be the one that was before returning frame"
        )

        self.assertTrue(
            setup_for_root_frame.stack.item_get_at(0) == returned_object,
            "When return_explicit opcode is executed, the top of root stack must be the value returned from returned frame"
        )

    def test_return_explicit_root_correct(self):
        # setup for root frame
        returned_object = object_kinds.VM_Symbol("to_be_returned", 0)

        setup_for_root_frame =_setup_process(
            literals_content=[],
            stack_content=[returned_object, None],
            bytecode_content=[Opcodes.RETURN_EXPLICIT, 0x00],
            none_object=None
        )

        # testing
        process = object_kinds.VM_Process(None, setup_for_root_frame.frame)
        interpreter = Interpreter(UniverseMockup(), process)
        interpreter.executeInstruction()

        self.assertTrue(
            process.peek_frame() is not setup_for_root_frame.frame,
            "When return_explicit opcode is executed in root frame, the active frame must not be the same as "
        )

        self.assertTrue(
            process.get_ordinary_result() == returned_object,
            "When return_explicit opcode is executed in root frame, the process result must be the return value from returning root frame"
        )

class InstructionSendTestCase(unittest.TestCase):
    def test_send_ordinary_object(self):
        slot_content = object_kinds.VM_Object()
        receiver =  object_kinds.VM_Object()
        slot_name = object_kinds.VM_Symbol("send_target", 0)
        receiver.add_slot(slot_name, SlotKind(), slot_content)

        setup= _setup_process(
            literals_content=[slot_name],
            stack_content=[receiver],
            bytecode_content=[Opcodes.SEND, 0x00],
            none_object=None
        )

        # testing
        process = object_kinds.VM_Process(None, setup.frame)
        interpreter = Interpreter(UniverseMockup(), process)
        interpreter.executeInstruction()

        self.assertTrue(
            setup.stack.item_get_at(0) is slot_content,
            "When send opcode is executed with ordinary object evaluated, the stack must contain the said ordinary object."

        )

    def test_send_nonparam_method_object(self):
        method = object_kinds.VM_Object()
        code = object_kinds.VM_Code(object_kinds.VM_ObjectArray(2, None), object_kinds.VM_ByteArray(2))
        method.set_code(code)

        receiver = object_kinds.VM_Object()
        slot_name = object_kinds.VM_Symbol("send_target", 0)
        receiver.add_slot(slot_name, SlotKind(), method)

        setup = _setup_process(
            literals_content=[slot_name],
            stack_content=[receiver],
            bytecode_content=[Opcodes.SEND, 0x00],
            none_object=None
        )

        process = object_kinds.VM_Process(None, setup.frame)
        interpreter = Interpreter(UniverseMockup(), process)
        interpreter.executeInstruction()

        self.assertTrue(
            process.peek_frame().get_previous_frame() is setup.frame,
            "When send opcode is executed with method object evaluated, the currently active frame must point to the frame in which instruction was executed."
        )

        self.assertTrue(
            process.peek_frame().get_method_activation().get_code() is code,
            "When send opcode is executed with method object evaluated, the current method activation must be copy of the method that was stored in target slot."
        )

    def test_send_param_method_object(self):
        parameter1 = object_kinds.VM_Symbol("param1", 0)
        argument1 = object_kinds.VM_SmallInteger(5)
        parameter2 = object_kinds.VM_Symbol("param2", 0)
        argument2 = object_kinds.VM_SmallInteger(10)

        method = object_kinds.VM_Object()
        code = object_kinds.VM_Code(object_kinds.VM_ObjectArray(2, None), object_kinds.VM_ByteArray(2))
        method.set_code(code)
        method.add_slot(parameter1, SlotKind().toggleParameter(), None)
        method.add_slot(parameter2, SlotKind().toggleParameter(), None)


        receiver = object_kinds.VM_Object()
        slot_name = object_kinds.VM_Symbol("send_target", 2)
        receiver.add_slot(slot_name, SlotKind(), method)

        setup = _setup_process(
            literals_content=[slot_name],
            stack_content=[receiver, argument1, argument2],
            bytecode_content=[Opcodes.SEND, 0x00],
            none_object=None
        )

        process = object_kinds.VM_Process(None, setup.frame)
        interpreter = Interpreter(UniverseMockup(), process)
        interpreter.executeInstruction()

        self.assertTrue(
            process.peek_frame().get_previous_frame() is setup.frame,
            "When send opcode is executed with parametric method object evaluated, the currently active frame must point to the frame in which instruction was executed."
        )

        self.assertTrue(
            process.peek_frame().get_method_activation().get_code() is code,
            "When send opcode is executed with parametric method object evaluated, the current method activation must be copy of the method that was stored in target slot."
        )

        self.assertTrue(
            process.peek_frame().is_stack_empty(),
            "When send opcode is executed with parametric method object evaluated, the stack must be empty."
        )

        self.assertTrue(
            process.peek_frame().get_method_activation().get_slot(parameter1) is argument1 and process.peek_frame().get_method_activation().get_slot(parameter2) is argument2,
        "When send opcode is executed with parametric method object evaluated, the parametric slots must contain correct argument content."
        )


if __name__ == '__main__':
    unittest.main()