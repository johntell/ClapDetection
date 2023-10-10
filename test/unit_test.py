import unittest
import os
import yaml

PATH_TO_DATA = "data/"

class TestStringMethods(unittest.TestCase):

    def test_alg1(self):
        for filename in os.listdir(PATH_TO_DATA):
            if filename.endswith(".wav"):
                print(filename)
                with open(PATH_TO_DATA + filename[:-3]+'yaml', 'r') as file:
                    data = yaml.safe_load(file)
                    print(data['clap_pattern'])
            else:
                continue

        
#        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
