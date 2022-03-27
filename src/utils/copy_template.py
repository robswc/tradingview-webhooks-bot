import os
from logging import getLogger, DEBUG

from utils.log import CONSOLE_HANDLER

logger = getLogger(__name__)
logger.addHandler(CONSOLE_HANDLER)
logger.setLevel(DEBUG)


def copy_from_template(source: str, target: str, tokens, replacements):
    """
    Copies template from source to target, includes replacements for any tokens
    :param source: source path
    :param target: target path
    :param tokens: strs to replace
    :param replacements: what to replace with
    """

    logger.debug(f'Starting copy of template {source.split("/")[-1]}...')
    logger.debug(f'Current working directory: {os.getcwd()}')

    # read in lines from source
    new_lines = []
    with open(source, 'r') as src_file:
        src_file_lines = src_file.readlines()
        logger.debug(f'{len(src_file_lines)} lines found in source file')
        for line in src_file_lines:
            new_line = line
            for idx, token in enumerate(tokens):
                if token in line:
                    new_line = new_line.replace(token, replacements[idx])

            new_lines.append(new_line)

    # write lines to target
    logger.debug(f'{target}')
    logger.debug(f'{len(new_lines)} new lines to write to -> {target.split("/")[-1]}')
    with open(target, 'w') as target_file:
        target_file.writelines(new_lines)
