from srcs.graph.or_state import OrState, OrStates
from srcs.goodbye import goodbye
from srcs.variables.named_variable import NamedVariable


class ExpressionSolver:
    solves = {}

    def __init__(self, graph):
        self.graph = graph

    def solve(self, letter, expressions, stops):
        local_solves = []
        if stops is None:
            stops = set()

        for expression in expressions:
            expression = expression.block
            stops.add(letter)
            result = self.solve_one_expression(expression, stops)
            local_solves.append(result)

        return self.choose_solve(local_solves, letter)

    def solve_one_expression(self, expression, letters):
        if isinstance(expression, NamedVariable):
            result = self.get_value(expression, letters)
        elif len(expression) == 3:
            result = self.solve_binary(expression, letters)
        elif len(expression) == 2:
            result = self.solve_unary(expression, letters)
        elif len(expression) == 1:
            result = self.get_value(expression, letters)
        return result

    def solve_binary(self, expression, letters):
        left_operand = self.solve_one_expression(expression.get_left_part(), letters)
        right_operand = self.solve_one_expression(expression.get_right_part(), letters)

        operator = expression.get_first_operator().source

        if (left_operand is None) or (right_operand is None):
            return None

        elif isinstance(left_operand, OrState) or isinstance(right_operand, OrState):
            return None

        actions = {
            '+': lambda x, y: x and y,
            '|': lambda x, y: x or y,
            '^': lambda x, y: x != y,
            '=>': lambda x, y: not (x and (not y)),
            '<=>': lambda x, y: x == y,
        }
        
        action = actions[operator]
        result = action(left_operand, right_operand)
        return result

    def solve_unary(self, expression, letters):
        operand = self.solve_one_expression(expression.get_left_part(), letters)

        operator = expression.get_first_operator().source

        if operand is None:
            return None

        elif isinstance(operand, OrState):
            return None

        actions = {
            '!': lambda x: not x,
        }

        action = actions[operator]
        result = action(operand)
        return result


    def get_value(self, expression, letters):
        operand_name = expression.get_left_part().source if not isinstance(expression, NamedVariable) else expression.source

        if operand_name in self.solves:
            return self.solves[operand_name]

        if operand_name in letters:
            return None

        node = self.graph.get_node(operand_name)

        result, from_source, letter = node.get_value(stops=letters)

        letters.add(operand_name)
        self.solves[operand_name] = result

        return result

    def choose_solve(self, solves, letter):
        bools = []
        nones = []
        ors = []

        for solve in solves:
            if isinstance(solve, bool):
                bools.append(solve)
            elif solve is None:
                nones.append(solve)
            elif isinstance(solve, OrState):
                ors.append(solve)

        if bools:
            first_bool = bools[0]
            for value in bools:
                if value != first_bool:
                    goodbye(f'A contradiction has been found for the variable {letter}.')
            return first_bool

        elif ors:
            return OrStates(states=ors)

        else:
            return None
