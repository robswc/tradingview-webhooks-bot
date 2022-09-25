import re

# configure logging
from logging import getLogger, DEBUG

from utils.log import get_logger

logger = get_logger(__name__)

class CustomName:
    def __init__(self, name):
        self.validate_name(name)
        self.name = name

    @staticmethod
    def validate_name(name):

        invalid_chars = ['_', ' ', '-']
        for c in invalid_chars:
            if c in name:
                raise ValueError(f'Name cannot contain "{c}"!  '
                                 f'Names must be CamelCase, i.e. "MyEvent" instead of "My{c}Event"')

        if any(not c.isalnum() for c in name):
            raise ValueError('String cannot contain special characters')

        logger.debug(f'Name: {name} passed validation!')

    def camel_case(self):
        return f'{self.name}'

    def snake_case(self):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', self.name).lower()
