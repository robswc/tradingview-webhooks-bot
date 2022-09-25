import importlib
import os
import time

from utils.formatting import snake_case
from utils.log import get_logger

logger = get_logger(__name__)


def validate_settings():
    """Validate settings.py"""
    import settings
    importlib.reload(settings)

    try:
        from settings import REGISTERED_ACTIONS
    except ImportError:
        logger.critical('REGISTERED_ACTIONS not found in settings.py')
        return False

    try:
        from settings import REGISTERED_EVENTS
    except ImportError:
        logger.critical('REGISTERED_EVENTS not found in settings.py')
        return False

    # make sure REGISTERED_ACTIONS is a list
    if not isinstance(REGISTERED_ACTIONS, list):
        logger.critical('REGISTERED_ACTIONS is not a list')
        return False

    # make sure REGISTERED_EVENTS is a list
    if not isinstance(REGISTERED_EVENTS, list):
        logger.critical('REGISTERED_EVENTS is not a list')
        return False

    # make sure REGISTERED_ACTIONS is a list of strings
    for action in REGISTERED_ACTIONS:
        if not isinstance(action, str):
            logger.critical(f'Action ({action}) is not a string')
            return False

    # make sure REGISTERED_EVENTS is a list of strings
    for event in REGISTERED_EVENTS:
        if not isinstance(event, str):
            logger.critical(f'Event ({event}) is not a string')
            return False

    # make sure all registered actions exist
    for action in REGISTERED_ACTIONS:
        try:
            cls = getattr(importlib.import_module(f'components.actions.{snake_case(action)}', action), action)()
        except ImportError:
            logger.critical(f'Action ({action}) not found')
            return False

    # make sure all registered events exist
    for event in REGISTERED_EVENTS:
        cls = getattr(importlib.import_module(f'components.events.{snake_case(event)}', event), event)()
        if not cls:
            logger.critical(f'Event ({event}) does not exist')
            return False

    return True


def cache_settings():
    """Cache settings.py"""
    settings_file = open('settings.py', 'r')
    settings_cache = settings_file.read()
    settings_file.close()
    return settings_cache


def build_settings(actions=None, events=None, links=None):
    """Build settings.py"""

    # settings cache
    settings_cache = cache_settings()

    # handle not provided
    if events is None:
        from settings import REGISTERED_EVENTS
        events = REGISTERED_EVENTS
    if actions is None:
        from settings import REGISTERED_ACTIONS
        actions = REGISTERED_ACTIONS
    if links is None:
        from settings import REGISTERED_LINKS
        links = REGISTERED_LINKS

    def wipe_settings():
        """Wipe settings.py"""
        logger.info('Resetting settings.py')
        settings_file = open('settings.py', 'w')
        settings_file.write('')
        settings_file.close()

    def write_variables(name, value, heading=None):
        """Write variables to settings.py"""
        settings_file = open('settings.py', 'a')
        settings_file.write(f'# {heading}\n{name} = {value}\n\n')
        settings_file.close()

    # first wipe settings.py
    wipe_settings()

    # write actions
    logger.debug(f'Writing ({len(actions)}) actions to settings.py')
    write_variables(name='REGISTERED_ACTIONS', value=actions, heading='actions')

    # write events
    logger.debug(f'Writing ({len(events)}) events to settings.py')
    write_variables(name='REGISTERED_EVENTS', value=events, heading='events')

    # write links
    logger.debug(f'Writing ({len(links)}) links to settings.py')
    write_variables(name='REGISTERED_LINKS', value=links, heading='links')

    # validate settings
    if validate_settings():
        logger.info('\n\n✓✓✓ Settings valid ✓✓✓\n')
    else:
        logger.error('\n\n✕✕✕ Settings not valid ✕✕✕\n')
        logger.error('Resetting settings.py')
        settings_file = open('settings.py', 'w')
        settings_file.write(settings_cache)
        settings_file.close()


def add_action(action_name):
    """Add action to settings.py"""

    actions = []
    try:
        from settings import REGISTERED_ACTIONS
        actions = REGISTERED_ACTIONS + [action_name]
    except ImportError:
        logger.error('Could not import REGISTERED_ACTIONS from settings.py')

    # use set to remove duplicates
    actions = list(set(actions))

    build_settings(actions=actions)


def delete_action(action_name):
    """Delete action from settings.py"""
    actions = []
    try:
        from settings import REGISTERED_ACTIONS
        actions = REGISTERED_ACTIONS
    except ImportError:
        logger.error('Could not import REGISTERED_ACTIONS from settings.py')

    if action_name in actions:
        actions.remove(action_name)
    else:
        logger.warning(f'Action ({action_name}) not found in settings.py')
    build_settings(actions=actions)


def add_event(event_name):
    """Add event to settings.py"""
    build_settings(events=[event_name])


def link_action_to_event(action_name, event_name):
    """Link action to event in settings.py"""

    try:
        from settings import REGISTERED_LINKS
    except ImportError:
        logger.error('Could not import REGISTERED_LINKS from settings.py')
        return

    links = REGISTERED_LINKS + [(action_name, event_name)]

    # use set to remove duplicates
    links = list(set(links))

    build_settings(links=links)


def unlink_action_to_event(action_name, event_name):
    """Unlink action to event in settings.py"""

    try:
        from settings import REGISTERED_LINKS
    except ImportError:
        logger.error('Could not import REGISTERED_LINKS from settings.py')
        return

    links = REGISTERED_LINKS

    if (action_name, event_name) in links:
        links.remove((action_name, event_name))
    else:
        logger.warning(f'Link ({action_name}, {event_name}) not found in settings.py')

    build_settings(links=links)
