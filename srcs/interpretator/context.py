class Context:
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data.get(self.convert_key(key), None)

    def __setitem__(self, key, value):
        self.data[self.convert_key(key)] = value

    def get(self, key, default):
        return self.data.get(self.convert_key(key), default)

    def convert_key(self, key):
        return key.lower()
