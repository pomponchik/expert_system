from srcs.variables.named_variable import NamedVariable
from srcs.variables.operators.unary_operator import UnaryOperator
from srcs.variables.operators.binary_operator import BinaryOperator
from srcs.variables.abstract_unit import AbstractUnit


class ExpressionBlock:
    def __init__(self, units, string):
        self.units = units
        self.string = string

    def __repr__(self):
        contains = ', '.join([f'"{unit.source}"' if isinstance(unit, AbstractUnit) else repr(unit) for unit in self.units])
        return f'{type(self).__name__}([{contains}])'

    def __str__(self):
        contains = ''.join([f'{unit.source}' if isinstance(unit, AbstractUnit) else f'({str(unit)})' for unit in self.units])
        return contains

    def __len__(self):
        return len(self.units)

    def is_final_or_state(self):
        if len(self) == 3 and isinstance(self.get_first_operand(), NamedVariable) and isinstance(self.get_second_operand(), NamedVariable):
            return True
        return False

    def is_simple(self):
        if len(self) == 1 and isinstance(self.units[0], NamedVariable):
            return True
        return False

    def copy(self):
        new_units = []

        for unit in self.units:
            if isinstance(unit, type(self)):
                unit = unit.copy()
            new_units.append(unit)

        return type(self)(new_units, self.string)

    def get_first_operand(self):
        for unit in self.units:
            if isinstance(unit, type(self)) or isinstance(unit, NamedVariable):
                return unit
        return None

    def get_second_operand(self):
        flag = False
        for unit in self.units:
            if isinstance(unit, type(self)) or isinstance(unit, NamedVariable):
                if not flag:
                    flag = True
                else:
                    return unit
        return None

    def get_right_part(self):
        if not len(self.units) == 3:
            return None
        return self.units[2]

    def get_left_part(self):
        if not len(self.units) == 3:
            return None
        return self.units[0]

    def get_variables(self):
        variables = set()
        self.get_variables_recursive(variables)
        return list(variables)

    def get_variables_recursive(self, variables):
        for unit in self.units:
            if isinstance(unit, type(self)):
                unit.get_variables_recursive(variables)
            elif isinstance(unit, NamedVariable):
                variables.add(unit.source)

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
        while len(self.units) == 1:
            if not isinstance(self.units[0], type(self)):
                break
            self.units = self.units[0].units

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

    def get_first_operator(self):
        for unit in self.units:
            if isinstance(unit, UnaryOperator) or isinstance(unit, BinaryOperator):
                return unit
        return None

    def get_all_operators(self):
        result = []
        for unit in self.units:
            if isinstance(unit, UnaryOperator) or isinstance(unit, BinaryOperator):
                result.append(unit)
        return result

    def check_order(self):
        if len(self.get_all_operators()) > 1:
            goodbye(f'Incorrect order of operators in the line {self.string.index}.')

        operator = self.get_first_operator()

        if isinstance(operator, UnaryOperator) and isinstance(self.units[0], UnaryOperator) and (isinstance(self.units[1], type(self)) or isinstance(self.units[1], NamedVariable)) and len(self.units) == 2:
            pass
        elif isinstance(operator, BinaryOperator) and isinstance(self.units[1], BinaryOperator) and (isinstance(self.units[0], type(self)) or isinstance(self.units[0], NamedVariable)) and (isinstance(self.units[2], type(self)) or isinstance(self.units[2], NamedVariable)) and len(self.units) == 3:
            pass
        elif operator is None and len(self.units) == 1 and (isinstance(self.units[0], NamedVariable) or isinstance(self.units[0], type(self))):
            pass
        elif not len(self.units):
            pass
        else:
            goodbye(f'Incorrect order of operators in the line {self.string.index}.')

        for unit in self.units:
            if isinstance(unit, type(self)):
                unit.check_order()
