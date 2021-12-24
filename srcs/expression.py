from srcs.variables.named_variable import NamedVariable
from srcs.variables.operators.unary_operator import UnaryOperator
from srcs.variables.operators.binary_operator import BinaryOperator
from srcs.variables.other import OtherUnit
from srcs.variables.abstract_unit import AbstractUnit
from srcs.goodbye import goodbye


class ExpressionBlock:
    def __init__(self, units, string):
        self.units = units
        self.string = string

    def __repr__(self):
        contains = ', '.join([f'"{unit.source}"' if isinstance(unit, AbstractUnit) else repr(unit) for unit in self.units])
        return f'{type(self).__name__}([{contains}])'

    def remove_extra_blocks(self):
        while len(self.units) == 1 and isinstance(self.units[0], type(self)):
            self.units = self.units[0].units

        for unit in self.units:
            if isinstance(unit, type(self)):
                unit.remove_extra_blocks()

    def separate_operations(self):
        operators_order = [
            '!',
            '+',
            '|',
            '^',
            '=>',
            '<=>',
        ]
        for operation_mark in operators_order:
            self.separate_operation(operation_mark)

    def separate_operation(self, operation_mark):
        result = []
        index = 0

        while index < len(self.units):
            unit = self.units[index]

            if isinstance(unit, type(self)):
                unit.separate_operation(operation_mark)
                result.append(unit)
                index += 1

            elif isinstance(unit, UnaryOperator) or isinstance(unit, BinaryOperator):
                if unit.source == operation_mark:
                    if isinstance(unit, UnaryOperator):
                        next_index = index + 1
                        if not (next_index < len(self.units)):
                            goodbye(f'Error in line {self.string.index}: Missing operand for operator "{unit.source}".')
                        next_unit = self.units[next_index]
                        new_unit = type(self)([unit, next_unit], self.string)
                        result.append(new_unit)
                        index += 2
                    if isinstance(unit, BinaryOperator):
                        if not result:
                            goodbye(f'Error in line {self.string.index}: Missing operand for operator "{unit.source}".')
                        next_index = index + 1
                        if not (next_index < len(self.units)):
                            goodbye(f'Error in line {self.string.index}: Missing operand for operator "{unit.source}".')
                        next_unit = self.units[next_index]
                        previous_unit = result.pop()
                        new_unit = type(self)([previous_unit, unit, next_unit], self.string)
                        result.append(new_unit)
                        index += 2
                else:
                    result.append(unit)
                    index += 1
            else:
                result.append(unit)
                index += 1

        self.units = result

    def separate_implications(self):
        number_of_implications = 0

        for unit in self.units:
            if isinstance(unit, BinaryOperator) and (unit.source == '=>' or unit.source == '<=>'):
                number_of_implications += 1

        if number_of_implications > 1:
            goodbye(f'Uncertainty in line {self.string.index}: the implication is duplicated.')

        self.number_of_implications = number_of_implications

        if number_of_implications != 1:
            return

        buffer = []
        new_units = []

        for unit in self.units:
            if isinstance(unit, BinaryOperator) and (unit.source == '=>' or unit.source == '<=>'):
                new_units.append(type(self)(buffer, self.string))
                new_units.append(unit)
                buffer = []
            else:
                buffer.append(unit)

        new_units.append(type(self)(buffer, self.string))

        self.units = new_units

    def is_empty(self):
        return len(self.units) == 0

    def clean_emptys(self):
        new_units = []
        for unit in self.units:
            if isinstance(unit, type(self)):
                unit.clean_emptys()
                if not unit.is_empty():
                    new_units.append(unit)
            else:
                new_units.append(unit)
        self.units = new_units

    def cut_breackets(self):
        if not self.check_breackets():
            goodbye(f'Incorrect order of parentheses in line {self.string.index}.')

        stack = []

        for unit in self.units:
            if isinstance(unit, AbstractUnit) and unit.source == ')':
                temp_units = []
                while stack:
                    maybe_open_breacket = stack.pop()
                    if isinstance(maybe_open_breacket, AbstractUnit) and maybe_open_breacket.source == '(':
                        break
                    else:
                        temp_units.append(maybe_open_breacket)
                temp_units.reverse()
                new_block = type(self)(temp_units, self.string)
                stack.append(new_block)
            else:
                stack.append(unit)

        self.units = stack

    def check_breackets(self):
        stack = []

        for unit in self.units:
            if isinstance(unit, AbstractUnit) and unit.source == ')':
                good = False
                while stack:
                    maybe_open_breacket = stack.pop()
                    if isinstance(maybe_open_breacket, AbstractUnit):
                        if maybe_open_breacket.source == '(':
                            good = True
                            break
                if not good:
                    return False
            else:
                stack.append(unit)

        for unit in stack:
            if unit.source == '(':
                return False

        return True

class Expression:
    def __init__(self, tokens, graph, string):
        self.tokens = tokens
        self.graph = graph
        self.block = self.create_units(tokens, graph, string)

    def is_active(self):
        return self.block.number_of_implications != 0

    def is_empty(self):
        return self.block.is_empty()

    def create_units(self, tokens, graph, string):
        units = self.convert_tokens_to_units(tokens, graph)
        block = ExpressionBlock(units, string)
        block.cut_breackets()
        block.clean_emptys()
        block.separate_implications()
        block.separate_operations()
        block.remove_extra_blocks()
        return block

    def convert_tokens_to_units(self, tokens, graph):
        units = {
            'binary': BinaryOperator,
            'unary': UnaryOperator,
            'named': NamedVariable,
            'other': BinaryOperator,
        }
        result = []
        for token in tokens:
            unit_type = units[token.type]
            unit = unit_type(token, graph)
            result.append(unit)
        return result

    def clone(self):
        pass
