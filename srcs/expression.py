from srcs.variables.named_variable import NamedVariable
from srcs.variables.operators.unary_operator import UnaryOperator
from srcs.variables.operators.binary_operator import BinaryOperator
from srcs.variables.other import OtherUnit
from srcs.variables.abstract_unit import AbstractUnit
from srcs.token import Token
from srcs.goodbye import goodbye
from srcs.expression_block import ExpressionBlock


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
