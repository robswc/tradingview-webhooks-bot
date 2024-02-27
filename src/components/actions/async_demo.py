from time import sleep

from components.actions.base.action import Action


class AsyncDemo(Action):
    def __init__(self):
        super().__init__()

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)  # this is required
        """
        Custom run method. Add your custom logic here.
        """
        print(self.name, '---> action has started...')
        for i in range(5):
            print(f'{self.name} ---> {i}')
            sleep(1)
        print(self.name, '---> action has completed!')
