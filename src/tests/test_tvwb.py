import os
from unittest import TestCase


class TestCLI(TestCase):
    # change dir before running tests

    os.chdir('..')

    def test_newevent(self):
        from tvwb import newevent
        assert newevent(name='TestEvent')
        self.assertRaises(ValueError, newevent, name='!')
        self.assertRaises(ValueError, newevent, name='@')
        self.assertRaises(ValueError, newevent, name='#')
        self.assertRaises(ValueError, newevent, name='test event')
        self.assertRaises(ValueError, newevent, name='test-event')
        self.assertRaises(ValueError, newevent, name='test_event')

    def test_newaction(self):
        from tvwb import newaction
        assert newaction(name='TestAction')
        self.assertRaises(ValueError, newaction, name='!')
        self.assertRaises(ValueError, newaction, name='@')
        self.assertRaises(ValueError, newaction, name='#')
        self.assertRaises(ValueError, newaction, name='test action')
        self.assertRaises(ValueError, newaction, name='test-action')
        self.assertRaises(ValueError, newaction, name='test_action')
