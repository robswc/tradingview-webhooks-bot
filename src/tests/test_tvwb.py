import os
from unittest import TestCase


class TestCLI(TestCase):

    def setUp(self) -> None:
        self.prefix = 'python tvwb.py'
        self.initial_settings = open('settings.py', 'r').read()

    def test_create_and_register_action(self):

        # create action
        cmd = f'{self.prefix} action:create CustomAction --no-register'
        try:
            os.system(cmd)
        except Exception as e:
            self.fail(e)

        # register action
        cmd = f'{self.prefix} action:register CustomAction'
        try:
            os.system(cmd)
        except Exception as e:
            self.fail(e)

    def tearDown(self) -> None:
        os.remove('components/actions/custom_action.py')

        # restore settings.py
        with open('settings.py', 'w') as settings_file:
            settings_file.write(self.initial_settings)
            settings_file.close()
