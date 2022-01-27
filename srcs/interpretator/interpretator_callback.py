from srcs.errors import InternalError


class InterpretatorCallback:
    def __init__(self, function, filter):
        self.function = function
        self.filter = filter if filter is not None else lambda x: True

    def __call__(self, string, string_number, context):
        if self.allowed(string):
            try:
                result = self.function(string, string_number, context)
                return None if result is None else f'\033[97m{result}\033[0m'
            except InternalError as e:
                return f'\033[31m{str(e)}\033[0m'
            except Exception as e:
                #print(type(e))
                #import traceback
                #print(traceback.format_exc())
                return f'\033[31moops! internal error ({e})\033[0m'

    def allowed(self, string):
        try:
            result = bool(self.filter(string))
            return result
        except:
            return False
