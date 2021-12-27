from srcs.graph.node import Node
from srcs.expression import Expression


class Graph:
    def __init__(self, rules, initial_facts):
        self.nodes = {}
        self.create_nodes(rules)
        self.facts_aware(initial_facts)

    def create_nodes(self, rules):
        for rule in rules:
            expression = Expression(rule.tokens, self, rule)
            if not expression.is_empty():
                if expression.is_active():
                    for one_expression in expression.clone():
                        if one_expression.is_solvable():
                            for simple_expression in one_expression.simplify():
                                print(simple_expression)
                                pass
                                #print(simple_expression.block)

    def facts_aware(self, initial_facts):
        pass
