import re
import string

VALID_SHORT_SYMBOLS = string.ascii_letters + string.digits
VALID_SHORT_PATTERN = f'^[{re.escape(VALID_SHORT_SYMBOLS)}]*$'

ORIGINAL_URL_LENGHT = 256
SHORT_URL_LENGHT = 16
RANDOM_SHORT_LENGHT = 6