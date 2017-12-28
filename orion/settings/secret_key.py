import os
from binascii import hexlify

KEY_LENGTH = 100
GENERATED_SECRET_KEY = hexlify(os.urandom(KEY_LENGTH))