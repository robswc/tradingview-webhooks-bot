from unittest import TestCase

from utils.modify_settings import build_settings, add_action, delete_action


class TestModifySettings(TestCase):
    def test_build_settings(self):
        try:
            build_settings()
        except Exception as e:
            self.fail(e)

    def test_add_action(self):
        try:
            add_action('CustomActionAgain')
        except Exception as e:
            self.fail(e)

    def test_delete_action(self):
        try:
            delete_action('CustomActionAgain')
        except Exception as e:
            self.fail(e)
