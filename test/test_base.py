import unittest
import string
import random

class TestBase(unittest.TestCase):

    @classmethod
    def generateRandomString(self, length):        
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string    