import unittest
import os
import yaml
from scipy.io.wavfile import read
import numpy as np

PATH_TO_DATA = "data/"

class TestStringMethods(unittest.TestCase):

    def test_alg1(self):
        for filename in os.listdir(PATH_TO_DATA):
            if filename.endswith(".wav"):
                print(filename)
                with open(PATH_TO_DATA + filename[:-3]+'yaml', 'r') as file:
                    data = yaml.safe_load(file)
                    print(data['clap_pattern'])

                    # Read the wave file
                    sample_rate, audio_data = read(PATH_TO_DATA+filename)

                    # Convert to mono if the audio file has 2 channels
                    if len(audio_data.shape) == 2:
                        audio_data = np.mean(audio_data, axis=1, dtype=int)

                    print(len(audio_data), sample_rate)
                    #TOdo: call clap_detect_alg1 and pattern_detect with BUFFER = 1024 samples from audio_data at a time until end of audio_data.
                    # padd audio_data with 0's if not mylitple of BUFFER =1024
                    # Check if clap_pattern from yaml matches with the calculated
            else:
                continue

        
#        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
