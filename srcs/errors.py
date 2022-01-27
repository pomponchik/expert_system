class InternalError(ValueError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'Error: {self.message}'
