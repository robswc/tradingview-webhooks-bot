import importlib
from importlib import import_module
import traceback

from utils.formatting import snake_case
from utils.log import get_logger

logger = get_logger(__name__)


def register_action(action_name):
    """
    Registers an action to the actions registry.
    :param action_name: str
    :param target_file: str
    :return: bool
    """
    logger.info(f'Registering action --->\t{action_name}')
    try:
        # snake case name
        snake_case_name = snake_case(action_name)
        # import the target file
        action = getattr(import_module(f'components.actions.{snake_case_name}', action_name), action_name)()
        logger.debug(f'Imported action module --->\t{snake_case_name}')
        # register the action
        action.register()
        logger.info(f'Action "{action_name}" registered successfully!')
        return action_name
    except Exception as e:
        logger.error(f'Action "{action_name}" failed to register!')
        logger.error(e)
        # print stack trace
        traceback.print_exc()


def register_event(event_name: str):
    """
    Registers an event to the events registry.
    :param event_name: str
    :param target_file: str
    :return: bool
    """
    logger.info(f'Registering event --->\t{event_name}')
    try:
        # snake case name
        snake_case_name = snake_case(event_name)
        # import the target file
        event = getattr(import_module(f'components.events.{snake_case_name}', event_name), event_name)()
        logger.debug(f'Imported event module --->\t{snake_case_name}')
        # register the event
        event.register()
        logger.info(f'Event "{event_name}" registered successfully!')
        return event
    except Exception as e:
        logger.error(f'Event "{event_name}" failed to register!')
        logger.error(e)
        # print stack trace
        traceback.print_exc()


def register_link(link: tuple, event_manager, action_manager):
    try:
        action = action_manager.get(link[0])
        event = event_manager.get(link[1])
        event.add_action(action)
        logger.info(f'Link "{link[0]} -> {link[1]}" registered successfully!')
        return True
    except Exception as e:
        logger.error(f'Link "{link[0]} -> {link[1]}" failed to register!')
        logger.error(e)
        # print stack trace
        traceback.print_exc()
