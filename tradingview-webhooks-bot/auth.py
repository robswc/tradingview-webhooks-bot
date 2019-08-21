import hashlib

"""
Planning to add more here eventually, for now will be used for handling keys.
"""

# Set this to something unique.
pin = '1234'


# Generate unique token from pin.  This adds a marginal amount of security.
def get_token():
    token = hashlib.sha224(pin.encode('utf-8'))
    return token.hexdigest()
