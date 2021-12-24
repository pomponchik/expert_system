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
                    print(expression.block)

    def facts_aware(self, initial_facts):
        pass
