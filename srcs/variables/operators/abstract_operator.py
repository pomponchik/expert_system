from srcs.variables.abstract_unit import AbstractUnit


class AbstractOperator(AbstractUnit):
    operands_number = None
    table = None

    def calculate(self, operands):
        result = self.table.get(operands, None)
        if result is None:
            pass

    def operands_is_basic(self, operands):
        for operand in operands:
            pass
