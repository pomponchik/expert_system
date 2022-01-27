class ConsoleRunner:
    def __init__(self, invitation):
        self.invitation = invitation

    def __call__(self, interpretator):
        while True:
            try:
                string = input(self.invitation)
                output = interpretator.execute(string)
                print(output)
            except KeyboardInterrupt:
                break
            except Exception:
                continue
        print('\033[34m\ngoodbye!\033[0m')
