import unittest
import os
import yaml
import sys
from scipy.io.wavfile import read
import numpy as np
from clap_detector import *

PATH_TO_DATA = "data/"

class TestStringMethods(unittest.TestCase):

    def test_alg1(self):
        num_tests = 0
        passed_tests = 0
        failed_tests = []
        for filename in os.listdir(PATH_TO_DATA):
            if filename.endswith(".wav"):
                num_tests = num_tests + 1
                print(filename)
                with open(PATH_TO_DATA + filename[:-3]+'yaml', 'r') as file:
                    last_clap_sample = 0
                    current_sample = 0 + DEBOUNCE_TIME_SAMPLES
                    clap_times = []
                    detected_patterns = []

                    data = yaml.safe_load(file)

                    # Read the wave file
                    sample_rate, audio_data = read(PATH_TO_DATA+filename)

                    # Convert to mono if the audio file has 2 channels
                    if len(audio_data.shape) == 2:
                        audio_data = np.mean(audio_data, axis=1, dtype=int)

                    audio_data.resize(len(audio_data)+RATE*2)

                    print(len(audio_data), sample_rate)

                    i = 0;
                    while i < len(audio_data):
                        current_sample = add_sample(current_sample, BUFFER)

                        if clap_detect_alg1(audio_data[i:i+BUFFER-1], current_sample, last_clap_sample):
                            last_clap_sample = current_sample
                            clap_times.append(current_sample)

                        result = pattern_detect(current_sample, clap_times)

                        if result:  # Non-empty result indicates a pattern was detected
                            detected_patterns.extend(result)  # Store the detected pattern
                            clap_times = []  # Reset clap_times only when a pattern was detected

                        i = i + BUFFER

                    print("expected_patterns %s" % str(data['clap_pattern']))
                    print("detected_patterns %s" % str(detected_patterns))
                    if data['clap_pattern'] == detected_patterns:
                        passed_tests = passed_tests + 1
                    else:
                        failed_tests.append({'filename': filename, 'expected': data['clap_pattern'], 'detected': detected_patterns})
                print('')
            else:
                continue

        print(failed_tests)
        self.assertEqual(passed_tests, num_tests)

if __name__ == '__main__':
    unittest.main()
