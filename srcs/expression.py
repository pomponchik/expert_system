from srcs.variables.named_variable import NamedVariable
from srcs.variables.operators.unary_operator import UnaryOperator
from srcs.variables.operators.binary_operator import BinaryOperator
from srcs.variables.other import OtherUnit
from srcs.variables.abstract_unit import AbstractUnit
from srcs.token import Token
from srcs.goodbye import goodbye


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

class Expression:
    def __init__(self, tokens, graph, string, from_tokens=True, from_expression=None):
        if from_tokens:
            self.from_expression = from_expression
            self.tokens = tokens
            self.graph = graph
            self.string = string
            self.block = self.create_units(tokens, graph, string)
        else:
            self.tokens = tokens
            self.graph = graph
            self.string = string
        self.from_expression = from_expression

    def is_solvable(self):
        operator = self.block.get_first_operator()
        if isinstance(operator, BinaryOperator) and (operator.source == '=>' or operator.source == '<=>'):
            return True
        return False

    def is_simple(self):
        right = self.block.get_right_part()
        if len(right) == 1:
            return True
        return False

    def simplify(self):
        if self.is_simple():
            return [self]

        old = [self]
        new = []

        flag = True

        while flag:
            flag = False
            for expression in old:
                expression.block.clean_emptys()
                operator = expression.block.get_right_part().get_first_operator()
                if operator is not None and operator.source in {'+', '!', '^'}:
                    flag = True
                    more_simples = self.get_simpler(expression)
                    for simple in more_simples:
                        new.append(simple)
                else:
                    new.append(expression)
            old = new
            new = []

        for expression in old:
            expression.block.clean_emptys()

        return old

    @staticmethod
    def get_simpler(expression):
        if expression.is_simple():
            return [expression]

        results = []

        left_block = expression.block.get_left_part()
        operator = expression.block.get_first_operator()
        right_block = expression.block.get_right_part()

        right_operator = right_block.get_first_operator()

        if right_operator.source == '!':
            new_expression = expression.create_copy()

            operand = right_block.get_first_operand()

            left_block = ExpressionBlock([right_operator, left_block], expression.string)
            right_block = ExpressionBlock([operand], expression.string)

            new_expression.block = ExpressionBlock([left_block, operator, right_block], expression.string)
            results.append(new_expression)

        elif right_operator.source == '+':
            expression_1 = expression.create_copy()
            expression_2 = expression.create_copy()

            operand_1 = right_block.get_first_operand()
            operand_2 = right_block.get_second_operand()

            expression_1.block = ExpressionBlock([ExpressionBlock([left_block, right_operator, operand_1], expression.string), operator, ExpressionBlock([operand_2], expression.string)], expression.string)
            expression_2.block = ExpressionBlock([ExpressionBlock([left_block, right_operator, operand_2], expression.string), operator, ExpressionBlock([operand_1], expression.string)], expression.string)

            results.append(expression_1)
            results.append(expression_2)

        elif right_operator.source == '^':
            expression_1 = expression.create_copy()
            expression_2 = expression.create_copy()

            operand_1 = right_block.get_first_operand()
            operand_2 = right_block.get_second_operand()

            negative_token = right_operator.token.copy()
            negative_token.source = '!'
            negative_token.size = 1
            negative_token.type = 'unary'
            negative_operator = UnaryOperator(negative_token, expression.graph)

            plus_token = right_operator.token.copy()
            plus_token.source = '+'
            plus_token.size = 1
            plus_token.type = 'binary'
            plus_operator = BinaryOperator(plus_token, expression.graph)

            left_1 = ExpressionBlock([left_block, plus_operator, ExpressionBlock([negative_operator, operand_1], expression.string)], expression.string)
            left_2 = ExpressionBlock([left_block, plus_operator, ExpressionBlock([negative_operator, operand_2], expression.string)], expression.string)

            expression_1.block = ExpressionBlock([left_1, operator, ExpressionBlock([operand_2], expression.string)], expression.string)
            expression_2.block = ExpressionBlock([left_2, operator, ExpressionBlock([operand_1], expression.string)], expression.string)

            results.append(expression_1)
            results.append(expression_2)
        else:
            results.append(expression)

        return results

    def create_copy(self):
        copy = type(self)(self.tokens, self.graph, self.string, from_tokens=False, from_expression=self)
        copy.block = self.block.copy()
        return copy

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
        block.check_order()
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
        expressions = []

        upper_operator = self.block.get_first_operator()

        if isinstance(upper_operator, BinaryOperator) and upper_operator.source == '<=>':
            clone_1 = self.create_copy()
            clone_2 = self.create_copy()

            units_clone_1 = []
            for unit in clone_1.block.units:
                if isinstance(unit, BinaryOperator):
                    token = unit.token.copy()
                    token.source = '=>'
                    units_clone_1.append(BinaryOperator(token, self.graph))
                else:
                    units_clone_1.append(unit)

            units_clone_2 = list(reversed(units_clone_1))

            clone_1.block = ExpressionBlock(units_clone_1, self.string)
            clone_2.block = ExpressionBlock(units_clone_2, self.string)

            expressions.append(clone_1)
            expressions.append(clone_2)
        else:
            expressions.append(self)

        return expressions

    def __str__(self):
        pre_result = []
        expression = self

        while expression:
            pre_result.append(str(self.block))
            expression = expression.from_expression

        result = ' from '.join(pre_result)
        return result
