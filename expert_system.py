from sys import argv

from srcs.reader import Reader
from srcs.goodbye import goodbye
from srcs.graph.graph import Graph
from srcs.result_interpreter import ResultInterpreter
from srcs.strings_group import StringsGroup
from srcs.string import String

from srcs.interpretator.interpretator import Interpretator
from srcs.interpretator.console_runner import ConsoleRunner
from srcs.settings import settings


def main():
    if len(argv) == 1:
        settings['interactive'] = True
        runner = ConsoleRunner(' >>> ')
        interpretator = Interpretator(runner)
        graph = Graph([], [])

        @interpretator()
        def responder(string, string_number, context):
            strings = StringsGroup([String(string, string_number)], check_order=False)

            rules = strings['rules']
            initial_facts = strings['initial_facts']
            queries = strings['queries']

            if len(rules):
                graph.create_nodes(rules)
                if '=' in string:
                    return 'rule added'
                else:
                    return 'empty rule'
            elif len(initial_facts):
                graph.facts_aware(initial_facts)
                return 'fact(s) added'
            elif len(queries):
                values = graph.get_values(queries)
                results = ResultInterpreter(values, graph).get_results()
                return '\n'.join(results)


        interpretator.run()

    elif len(argv) == 2:
        path = argv[1]
        strings_group = Reader(path).get_strings()

        rules = strings_group['rules']
        initial_facts = strings_group['initial_facts']
        queries = strings_group['queries']

        graph = Graph(rules, initial_facts)

        values = graph.get_values(queries)

        results = ResultInterpreter(values, graph).get_results()
        for result in results:
            print(result)
    else:
        goodbye('Incorrect input. Usage: python3 expert_system.py [path_to_source]')



if __name__ == '__main__':
    main()
