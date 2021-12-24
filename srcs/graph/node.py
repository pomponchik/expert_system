class Node:
    def __init__(self, name, graph):
        self.name = name
        self.graph = graph
        self.codes = []

    def add_final_state(self, state):
        maybe_conflicts_state = self.get_state()

    def add_code(self, code):
        self.codes.append(code)

    def get_state(self):
        pass
