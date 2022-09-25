from unittest import TestCase

from utils.register import register_action


class TestRegistering(TestCase):
    def test_register_action(self):
        register_action('custom_action')
        assert True
