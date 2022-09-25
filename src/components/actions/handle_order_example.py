from components.actions.base.action import Action


class HandleOrderExample(Action):
    def __init__(self):
        super().__init__()
        self.name = 'handle_order_example'

    def run(self, *args, **kwargs):
        super(Action).run(*args, **kwargs)
        """
        Custom run method. Add your custom logic here.
        """
        print(self.name, '---> action has run!')


handle_order_example = HandleOrderExample()
