from srcs.interpretator.interpretator_callback import InterpretatorCallback
from srcs.interpretator.context import Context

class Interpretator:
    def __init__(self, runner, meta=None):
        self.runner = runner
        self.meta = meta
        self.callbacks = []
        self.context = Context()
        self.current_string_index = 0
        self.strings = []

    def __call__(self, filter=None):
        def decorator(function):
            self.callbacks.append(InterpretatorCallback(function, filter))
            return function
        return decorator

    def execute(self, string):
        result = []

        for callback in self.callbacks:
            single_output = callback(string, self.current_string_index, self.context)
            if single_output is not None:
                result.append(single_output)

        self.current_string_index += 1
        self.strings.append(string)

        return '\n'.join(result)

    def run(self):
        self.runner(self)
