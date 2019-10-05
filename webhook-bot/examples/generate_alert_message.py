from auth import get_token

"""
This function will take a lot of the tedious work out of generating alert messages!
Simply follow the onscreen input prompts, at the end a string with everything you need
will be output, allowing you to copy and paste into tradingview!
"""


def generate_alert_message():
    print('Enter type: (limit, market, etc.)')
    type = input()
    print('Enter Side (buy or sell):')
    side = input()
    print('Enter Amount:')
    amount = input()
    print('Enter Symbol:')
    symbol = input()
    if type == 'limit':
        print('Enter limit price:')
        price = input()
    else:
        price = 'None'
    key = get_token()

    print("Copy:\n")
    output = {"type": type, "side": side, "amount": amount, "symbol": symbol, "price": price, "key": key}
    print(str(output).replace('\'', '\"'))


generate_alert_message()
