from components.actions.base.action import Action


class PrintData(Action):
    def __init__(self):
        super().__init__()

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)  # this is required
        """
        Custom run method. Add your custom logic here.
        """
        print(self.name, '---> action has run!')
        data = self.validate_data()  # always get data from webhook by calling this method!
        print('Data from webhook:', data)
