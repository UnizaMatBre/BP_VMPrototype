
from source.vm_core import instructions
from source.vm_core.object_kinds import VM_Proces


def _unknown_opcode(interpreter, parameter):
    """
    Tells interpreter that unknown opcode was encountered
    TODO: Implement body when implementing error handling
    """
    raise NotImplementedError()

"""
List that maps all possible opcode values (both valid and invalid) to specific operations.
First we will fill it with "unknown_opcode" mapping and then we manually set mapping for each valid opcode
"""
OPCODE_MAPPING = [_unknown_opcode] * 0xFF

OPCODE_MAPPING[instructions.Opcodes.NOOP] = lambda interpreter, parameter: interpreter._do_nothing(parameter)
OPCODE_MAPPING[instructions.Opcodes.PUSH_MYSELF] = lambda interpreter, parameter: interpreter._do_push_myself(parameter)
OPCODE_MAPPING[instructions.Opcodes.PUSH_LITERAL] = lambda interpreter, parameter: interpreter._do_push_literal(parameter)
OPCODE_MAPPING[instructions.Opcodes.PULL] = lambda interpreter, parameter: interpreter._do_pull(parameter)
OPCODE_MAPPING[instructions.Opcodes.SEND] = lambda interpreter, parameter: interpreter._do_send(parameter)
OPCODE_MAPPING[instructions.Opcodes.RETURN_EXPLICIT] = lambda interpreter, parameter: interpreter._do_return_explicit(parameter)


class Interpreter:
    def __init__(self, process):
        assert isinstance(process, VM_Proces)

        self._my_process = process

    def _do_nothing(self, parameter):
        """Instruction that does nothing"""
        pass

    def _do_push_myself(self, parameter):
        """Takes method activation and pushes it to stack of active frame"""
        self.getActiveFrame().push_item(self.getActiveFrame().getMethodActivation())

    def _do_push_literal(self, parameter):
        """
        Takes object from array of literals, copies it and pushes copy into stack of active frame

        :param parameter: index into array of literals
        :return: None
        """

        # TODO: Handle possible error of index being out of the bound
        literal_original = self.getActiveFrame().literal_get_at(parameter)

        # TODO: Finish copying so that this instruction can properly work
        literal_copy = literal_original

        # TODO: Handle possible error of stack being full
        self.getActiveFrame().push_item(literal_copy)


    def _do_pull(self, parameter):
        """Pulls object from stack of active frame and discards it"""
        # TODO: Handle possible error of stack being empty
        # TODO: Pass proper none_object into pull
        self.getActiveFrame().pull_item(None)

    def _do_send(self, parameter):
        raise NotImplementedError()

    def _do_return_explicit(self, parameter):
        """Passes control and top of the stack from active frame to its predecessor"""



        # TODO: Handle possibility of this being the last frame
        returning_frame = self._my_process.pull_frame(None)

        # TODO: How should i handle empty stack? Error sounds too harsh - maybe returns none_object if stack is empty?
        # TODO: Pass proper none_object into pull
        # TODO: maybe this entire thing should be in "pull_frame" method
        stack_top = returning_frame.pull_item(None)

        # TODO: Handle possible error of stack being full
        self.getActiveFrame().push_item(stack_top)


    def getActiveFrame(self):
        return self._my_process.peek_frame()

    def executeInstruction(self):
        """
        Takes current instruction from active frame and executes it
        :return: None
        """
        opcode, parameter = self.getActiveFrame().get_current_instruction()

        # much faster than if-else spam
        OPCODE_MAPPING[opcode](self, parameter)
