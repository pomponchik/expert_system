class ResultInterpreter:
    def __init__(self, values, graph):
        self.values = values
        self.graph = graph

    def get_results(self):
        result = []
        for value, source, letter in self.values.values():
            result.append(self.get_result(value, source, letter))
        return result

    def get_result(self, value, source, letter):
        converted_value = self.convert_value(value)

        if source == 'default':
            return f'{letter} = {converted_value} (by default)'
        elif source == 'facts':
            return f'{letter} = {converted_value} (initialization fact)'
        elif source == 'expression':
            if isinstance(value, bool):
                converted_expressions = self.convert_expressions(self.graph.get_node(letter).simples)
                return f'{letter} = {converted_value} (from expression):\n{converted_expressions}'[:-1]
            else:
                return f'{letter} is defined in the following expressions: {converted_value}'

    def convert_expressions(self, expressions):
        results = []
        for expression in expressions:
            expression = expression.expression
            results.append(f'\t{expression.block}\n')
        return ''.join(results)

    def convert_value(self, value):
        if isinstance(value, bool):
            converters = {
                True: 'TRUE',
                False: 'FALSE',
            }
            return converters[value]
        else:
            return self.or_states_converter(value)

    def or_states_converter(self, value):
        return ', '.join([f'{state.block.get_left_part()} OR {state.block.get_right_part()}' for state in value.states])
