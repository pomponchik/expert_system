from sys import argv
from srcs.reader import Reader
from srcs.goodbye import goodbye


def main():
    if len(argv) != 2:
        goodbye('Incorrect input. Usage: python3 expert_system.py [path_to_source]')

    path = argv[1]
    strings_group = Reader(path).get_strings()

    rules = strings_group['rules']
    initial_facts = strings_group['initial_facts']
    queries = strings_group['queries']

    graph = Graph(rules, initial_facts)



    for string in initial_facts:
        print(string.clean_source, string.type)


if __name__ == '__main__':
    main()
