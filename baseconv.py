# utils/baseconv.py

import string

class BaseConverter:
    decimal_digits = string.digits
    digits = None

    def __init__(self, digits):
        self.digits = digits

    def encode(self, number):
        if number == 0:
            return self.digits[0]
        result = ''
        while number:
            number, remainder = divmod(number, len(self.digits))
            result = self.digits[remainder] + result
        return result

    def decode(self, encoded):
        result = 0
        for char in encoded:
            result = result * len(self.digits) + self.digits.index(char)
        return result

# Base36 example (0-9 + a-z)
base36 = BaseConverter(string.digits + string.ascii_lowercase)
