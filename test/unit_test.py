import unittest
import os

PATH_TO_DATA = "data"

class TestStringMethods(unittest.TestCase):

    def test_alg1(self):
        for filename in os.listdir(PATH_TO_DATA):
            if filename.endswith(".wav"):
                print(filename)
                continue
            else:
                continue

        
#        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
