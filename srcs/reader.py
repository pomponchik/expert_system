from srcs.goodbye import goodbye
from srcs.string import String
from srcs.strings_group import StringsGroup


class Reader:
    """
    Здесь происходит чтение файла.
    """
    def __init__(self, filename):
        self.filename = filename

    def get_strings(self):
        try:
            result = []

            with open(self.filename, 'r') as file:
                for index, source_string in enumerate(file):
                    string = String(source_string, index)
                    if not string.is_empty:
                        result.append(string)

            return StringsGroup(result)

        except Exception as e:
            raise e
            goodbye('The file could not be opened. There are three interpretations: you are an idiot, you are trying to break the program, or something is wrong with the file for reasons beyond your control.')
