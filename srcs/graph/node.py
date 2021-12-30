from srcs.graph.link import Link
from srcs.graph.fact import Fact
from srcs.graph.or_state import OrState, OrStates
from srcs.expression_solver import ExpressionSolver
from srcs.goodbye import goodbye


class Node:
    def __init__(self, name, graph):
        self.name = name
        self.graph = graph
        self.simples = []
        self.facts = []
        self.ors = []
        self.solver = ExpressionSolver(graph)

    def add_or(self, or_block, block, expression):
        link = Link(block=block, or_block=or_block, expression=expression)
        self.ors.append(link)

    def add_default(self, default, string):
        fact = Fact(value=default, string=string)
        self.facts.append(fact)

    def add_simple(self, simple, expression):
        link = Link(block=simple, expression=expression)
        self.simples.append(link)

    def get_value(self, stops=None):
        value_from_expression = self.get_value_from_expression(stops)
        value_from_facts = self.get_value_from_facts(stops)
        if isinstance(value_from_expression, bool):
            if isinstance(value_from_facts, bool):
                if value_from_expression != value_from_facts:
                    goodbye(f'A contradiction has been found for the variable {self.name}.')
            return value_from_expression, 'expression'
        elif value_from_expression is None:
            if isinstance(value_from_facts, bool):
                return value_from_facts, 'facts'
            return False, 'default'
        elif isinstance(value_from_expression, OrStates):
            if isinstance(value_from_facts, bool):
                return value_from_facts, 'facts'
            return value_from_expression, 'expression'

    def get_value_from_expression(self, stops):
        return self.solver.solve(self.name, self.simples, stops)

    def get_value_from_facts(self, stops):
        if not self.facts:
            return None

        first_fact = self.facts[0]

        for fact in self.facts:
            if fact.value != first_fact.value:
                goodbye(f'A contradiction has been found for the variable {self.name}.')

        return first_fact.value
