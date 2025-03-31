from object_kinds import VM_Proces


class Interpreter:
    def __init__(self, process):
        assert isinstance(process, VM_Proces)

        self._my_process = process


    def _do_nothing(self, parameter):
        raise NotImplementedError()

    def _do_push_myself(self, parameter):
        raise NotImplementedError()

    def _do_push_literal(self, parameter):
        raise NotImplementedError()

    def _do_pull(self, parameter):
        raise NotImplementedError()

    def _do_send(self, parameter):
        raise NotImplementedError()

    def _do_return_explicit(self, parameter):
        raise NotImplementedError()

    def executeInstruction(self):
        raise NotImplementedError()
