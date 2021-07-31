import sys
from actions.utils.action_manager import am
from events.utils.event_manager import em


def error(msg):
    print('\n[ERROR]\t{}'.format(msg))


def main(command):
    print(command)
    if command[1] == 'help':
        print("\nInformation on using manage.py to create actions and events:")
        print("https://github.com/robswc/tradingview-webhooks-bot/wiki/Using-Manage-to-Create-Events-and-Actions")
    if command[1] == 'create':
        # action branch
        if command[2] == 'action':
            # check args for proper format
            if (not command[3][0].isupper()) or not str(command[3]).isalnum():
                error(
                    '"Name" argument must be alphanumeric and start with an uppercase letter. ({})'.format(command[3]))
                sys.exit(1)
            if ' ' in command[4]:
                error('"File name cannot contain spaces or special characters.')

            # create action/file
            am.create_action(command[3], command[4].lower())

        # event branch
        if command[2] == 'event':
            # check args for proper format
            if (not command[3][0].isupper()) or not str(command[3]).isalnum():
                error(
                    '"Name" argument must be alphanumeric and start with an uppercase letter. ({})'.format(command[3]))
                sys.exit(1)
            if ' ' in command[4]:
                error('"File name cannot contain spaces or special characters.')

            # create action/file
            em.create_event(command[3], command[4].lower())


if __name__ == '__main__':
    main(sys.argv)
