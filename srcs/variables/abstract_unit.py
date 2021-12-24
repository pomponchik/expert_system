class AbstractUnit:
    def __init__(self, token, graph):
        self.token = token
        self.source = self.token.source
        self.graph = graph

    def __repr__(self):
        return f'{type(self).__name__}("{self.source}")'
