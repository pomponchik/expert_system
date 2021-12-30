from srcs.graph.node import Node
from srcs.expression import Expression


class Graph:
    def __init__(self, rules, initial_facts):
        self.nodes = {}
        self.create_nodes(rules)
        self.facts_aware(initial_facts)

    def get_node(self, literal):
        node = self.nodes.get(literal, None)
        if node is None:
            self.nodes[literal] = Node(literal, self)
            node = self.nodes[literal]
        return node

    def create_nodes(self, rules):
        for rule in rules:
            expression = Expression(rule.tokens, self, rule)
            if not expression.is_empty():
                if expression.is_active():
                    for one_expression in expression.clone():
                        if one_expression.is_solvable():
                            for simple_expression in one_expression.simplify():
                                simple_expression.check_tautology()
                                self.put_to_node(simple_expression)

    def put_to_node(self, expression):
        right_part = expression.block.get_right_part()
        left_part = expression.block.get_left_part()
        if right_part.is_simple():
            literal = right_part.units[0].source
            node = self.get_node(literal)
            node.add_simple(left_part, expression)
        elif right_part.is_final_or_state():
            pass

    def facts_aware(self, initial_facts):
        for facts in initial_facts:
            literals = facts.clean_source[1:]
            for literal in literals:
                node = self.get_node(literal)
                node.add_default(True, facts)

    def get_values(self, values_strings):
        names = set()

        for string in values_strings:
            string = string.clean_source
            string = string[1:]
            for letter in string:
                names.add(letter)

        results = {}

        for letter in names:
            node = self.get_node(letter)
            result = node.get_value()
            results[letter] = result

        return results
