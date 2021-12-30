from sys import argv

from srcs.reader import Reader
from srcs.goodbye import goodbye
from srcs.graph.graph import Graph


def main():
    if len(argv) != 2:
        goodbye('Incorrect input. Usage: python3 expert_system.py [path_to_source]')

    path = argv[1]
    strings_group = Reader(path).get_strings()

    rules = strings_group['rules']
    initial_facts = strings_group['initial_facts']
    queries = strings_group['queries']

    graph = Graph(rules, initial_facts)
    print(graph.nodes)

    values = graph.get_values(queries)

    print(values)



if __name__ == '__main__':
    main()
