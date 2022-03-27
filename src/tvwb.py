from logging import getLogger, DEBUG

import typer
from subprocess import run

from utils.copy_template import copy_from_template
from utils.log import CONSOLE_HANDLER
from utils.validators import CustomName

app = typer.Typer()

# configure logging
logger = getLogger(__name__)
logger.addHandler(CONSOLE_HANDLER)
logger.setLevel(DEBUG)


@app.command()
def start():
    run('gunicorn --bind 0.0.0.0:5000 wsgi:app'.split(' '))


@app.command()
def newaction(name: str):
    logger.info(f'Creating new action --->\t{name}')

    # validate name
    custom_name = CustomName(name)

    # begin copying of template to new target file
    copy_from_template(
        source=f'components/actions/base/template/action_template.py',
        target=f'components/actions/{custom_name.snake_case()}.py',
        tokens=['_TemplateAction_', 'TemplateActionClass', 'template_action'],
        replacements=[custom_name.snake_case(), custom_name.camel_case(), custom_name.snake_case()])

    logger.info(f'Event "{name}" created successfully!')
    return True


@app.command()
def newevent(name: str):
    logger.info(f'Creating new event --->\t{name}')

    # validate name
    custom_name = CustomName(name)

    # begin copying of template to new target file
    copy_from_template(
        source=f'components/events/base/template/event_template.py',
        target=f'components/events/{custom_name.snake_case()}.py',
        tokens=['_TemplateEvent_', 'TemplateEventClass', 'template_event'],
        replacements=[f'{custom_name.snake_case()}', custom_name.camel_case(), custom_name.snake_case()])

    logger.info(f'Event "{name}" created successfully!')
    return True


if __name__ == "__main__":
    app()
