import re


def snake_case(text):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()