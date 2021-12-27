from srcs.graph.link import Link
from srcs.graph.fact import Fact
from srcs.goodbye import goodbye


class Node:
    def __init__(self, name, graph):
        self.name = name
        self.graph = graph
        self.simples = []
        self.defaults = []
        self.ors = []

    def add_or(self, or_block, block, expression):
        link = Link(block=block, or_block=or_block, expression=expression)
        self.ors.append(link)

    def add_default(self, default, string):
        fact = Fact(value=default, string=string)
        self.defaults.append(fact)

    def add_simple(self, simple, expression):
        link = Link(block=simple, expression=expression)
        self.simples.append(link)

    def get_value(self):
        pass
