
from source.vm_core import bytecodes
from source.vm_core.object_kinds import VM_Process, VM_Assignment, VM_PrimitiveMethod, VM_Symbol
from source.vm_core.object_layout import VM_Object, SlotKind


def _unknown_opcode(interpreter, parameter):
    """
    Tells interpreter that unknown opcode was encountered
    """
    interpreter._handle_process_error("unknownOpcode")

"""
List that maps all possible opcode values (both valid and invalid) to specific operations.
First we will fill it with "unknown_opcode" mapping and then we manually set mapping for each valid opcode
"""
OPCODE_MAPPING = [_unknown_opcode] * 0xFF

OPCODE_MAPPING[bytecodes.Opcodes.NOOP] = lambda interpreter, parameter: interpreter._do_nothing(parameter)
OPCODE_MAPPING[bytecodes.Opcodes.PUSH_MYSELF] = lambda interpreter, parameter: interpreter._do_push_myself(parameter)
OPCODE_MAPPING[bytecodes.Opcodes.PUSH_LITERAL] = lambda interpreter, parameter: interpreter._do_push_literal(parameter)
OPCODE_MAPPING[bytecodes.Opcodes.PULL] = lambda interpreter, parameter: interpreter._do_pull(parameter)
OPCODE_MAPPING[bytecodes.Opcodes.SEND] = lambda interpreter, parameter: interpreter._do_send(parameter)
OPCODE_MAPPING[bytecodes.Opcodes.RETURN_EXPLICIT] = lambda interpreter, parameter: interpreter._do_return_explicit(parameter)


class Interpreter:
    def __init__(self, universe, process):
        assert isinstance(process, VM_Process)

        self._universe = universe
        self._my_process = process


    def _get_none_object(self):
        return self._universe.get_none_object()


    def get_active_frame(self):
        return self._my_process.peek_frame()

    def get_universe(self):
        return self._universe

    def _handle_process_error(self, symbol_text):
        """
        Handles error that is concerning entire process.
        In current implementation, that means it will terminate process with error object as result

        :param symbol_text: name of error
        :return: None
        """
        error_symbol = self._universe.new_symbol(symbol_text, 0)
        error_obj = self._universe.new_error_object(error_symbol)

        self._my_process.set_result(error_obj)

    def _do_nothing(self, parameter):
        """Instruction that does nothing"""
        pass

    def _do_push_myself(self, parameter):
        """Takes method activation and pushes it to stack of active frame"""
        self.get_active_frame().push_item(self.get_active_frame().get_method_activation())

    def _do_push_literal(self, parameter):
        """
        Takes object from array of literals, copies it and pushes copy into stack of active frame

        :param parameter: index into array of literals
        :return: None
        """

        if self.get_active_frame().is_stack_full():
            self._handle_process_error("stackOverflow")
            return

        ok, literal_original = self.get_active_frame().literal_get_at(parameter)

        if not ok:
            self._handle_process_error("literalIndexOutOfBound")
            return

        literal_copy = literal_original.copy()

        self.get_active_frame().push_item(literal_copy)


    def _do_pull(self, parameter):
        """Pulls object from stack of active frame and discards it"""
        if self.get_active_frame().is_stack_empty():
            self._handle_process_error("stackUnderflow")
            return


        self.get_active_frame().pull_item(self._get_none_object())

    def _do_send(self, parameter):
        """
        Takes arguments and receiver from stack, looks up slot and evaluates its content.

        :param parameter: index of message selector in array of literals
        :return: None
        """

        ok, selector = self.get_active_frame().literal_get_at(parameter)

        if not ok:
            self._handle_process_error("literalIndexOutOfBound")
            return

        if not isinstance(selector, VM_Symbol):
            self._handle_process_error("notSymbolicSelector")
            return

        # check if there is enough stack items to extract receivers and arguments
        if not self.get_active_frame().can_stack_change_by(-(selector.get_arity() + 1)):
            self._handle_process_error("stackUnderflow")
            return

        # arguments extraction - parameter list is filled from the end because last parameter is at the top of stack
        arguments = [None] * selector.get_arity()
        for index in reversed(range(selector.get_arity())):
            arguments[index] = self.get_active_frame().pull_item(self._get_none_object())

        # receiver extraction
        receiver = self.get_active_frame().pull_item(self._get_none_object())

        assert isinstance(receiver, VM_Object)

        # TODO: handle possible error of slot not being found
        lookup_status, lookup_slot_location = receiver.lookup_slot(selector)

        slot_content = lookup_slot_location.get_slot(selector)

        ## evaluate slot content
        # evaluate assignment primitive
        if isinstance(slot_content, VM_Assignment):
            # TODO: Handle possible error of slot not existing
            lookup_slot_location.set_slot(slot_content.get_target_name(), arguments[0])


            # there is no need to check if stack has space - if it had space for send itself, it has space for result
            self.get_active_frame().push_item(arguments[0])

        # evaluate primitive method
        if isinstance(slot_content, VM_PrimitiveMethod):
            result = slot_content.native_call(self, arguments)

            self.get_active_frame().push_item(result)

            return

        # has code? Evaluate method object
        if slot_content.has_code():
            method_activation = slot_content.copy()

            parameter_slots = method_activation.select_slots(lambda name, kind, content: kind.isParameter())

            for index in range(len(arguments)):
                parameter_name, _, _ = next(parameter_slots)

                # TODO: Handle possible error of parameter param count and slot arity don't match
                method_activation.set_slot(parameter_name, arguments[index])

            # insert scope
            # TODO: This needs to be more solid
            method_activation.add_slot(
                self._universe.new_symbol("me", 0),
                SlotKind().toggleParent(),
                receiver
            )

            self._my_process.push_frame(
                self._universe.new_frame_with_stack_size(
                    method_activation.get_code().get_stack_usage(),
                    method_activation
                )
            )

            return

        # evaluate everything else (which means 'push to the stack')
        if self.get_active_frame().is_stack_full():
            self._handle_process_error("stackOverflow")
            return

        self.get_active_frame().push_item(slot_content)


    def _do_return_explicit(self, parameter):
        """Passes control and top of the stack from active frame to its predecessor"""


        if self.get_active_frame().is_stack_empty():
            self. _handle_process_error("stackUnderflow")
            return

        # get return value and remove frame from proces
        the_return_value = self.get_active_frame().pull_item(self._universe.get_none_object())
        self._my_process.pull_frame(self._get_none_object())

        # no more frames? Return value is process result
        if self.get_active_frame() is self._get_none_object():
            self._my_process.set_result(the_return_value)
            return

        # current frame is full? Stack overflow
        if self.get_active_frame().is_stack_full():
            self._handle_process_error("stackOverflow")
            return

        self.get_active_frame().push_item(the_return_value)




    def execute_instruction(self):
        """
        Takes current instruction from active frame and executes it
        :return: None
        """
        # don't execute instructions of already finished process
        if self._my_process.has_finished(self._universe.get_none_object()):
            return

        # get rid of finished frame
        if self.get_active_frame().has_finished():
            self._do_return_explicit(0)
            return

        # extract instruction (opcode and its parameter)
        opcode, parameter = self.get_active_frame().get_current_instruction()

        # move instruction index forward
        self.get_active_frame().move_instruction_by(1)

        # much faster than if-else spam
        OPCODE_MAPPING[opcode](self, parameter)
