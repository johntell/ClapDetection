import pyaudio
import numpy as np
import time
import requests
from scipy.signal import butter, lfilter, find_peaks

# Constants
VOLUME_THRESHOLD = 5000
RATE = 44100
BUFFER = 1024
DEBOUNCE_TIME = 0.15  # seconds
RESET_TIME = 1.0  # seconds to reset the clap pattern

# Initialize the state to False (Light Off)
light_state = False

# Initialize PyAudio and Stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=BUFFER)

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    filtered_data = lfilter(b, a, data)
    return filtered_data

def compute_frequencies(audio_data):
    fft_data = np.fft.fft(audio_data)
    magnitude = np.abs(fft_data)
    frequencies = np.fft.fftfreq(len(fft_data), 1.0/RATE)
    return frequencies, magnitude

last_clap_time = time.time() - DEBOUNCE_TIME
clap_times = []

def clap_detect_alg1(audio_data, current_time, last_clap_time):
    clap_detected = False

    # Apply bandpass filter to focus on clap frequencies
    filtered_audio = bandpass_filter(audio_data, lowcut=2000, highcut=2800, fs=RATE)

    # Find peaks in the audio signal
    peaks, _ = find_peaks(filtered_audio, height=VOLUME_THRESHOLD)

    # If peaks are found and debounce time has passed
    if len(peaks) > 0 and (current_time - last_clap_time >= DEBOUNCE_TIME):
        print(f"Clap detected! {len(peaks)} peaks found")
        clap_detected = True

    return clap_detected

def pattern_detect(current_time, clap_times):
    # Check for pattern reset
    if clap_times and (current_time - clap_times[-1] >= RESET_TIME):
        intervals = [clap_times[i] - clap_times[i-1] for i in range(1, len(clap_times))]
        pattern = ["clap"]
        for interval in intervals:
            symbol = " - " if interval < 0.5 else " _ "
            pattern.append(symbol + "clap")
        pattern_str = "".join(pattern)
        print("Pattern:", pattern_str)
        return pattern_str
    return ''

try:
    while True:
        input_data = stream.read(BUFFER)
        audio_data = np.frombuffer(input_data, dtype=np.int16)
        current_time = time.time()
        if clap_detect_alg1(audio_data, current_time, last_clap_time):
            last_clap_time = current_time
            clap_times.append(current_time)

        result = pattern_detect(current_time, clap_times)

        if result == "clap - clap":
            light_state = not light_state
            url = "http://192.168.50.91/api/MGHLl7IZa-qnZJH9GC8DT9bEeUgnywktYFWtMR9T/groups/1/action"
            payload = {"on": light_state}
            headers = {"Content-Type": "application/json"}
            response = requests.request("PUT", url, json=payload, headers=headers)
            print(response.text)

        if result is not '':
            clap_times = []  # Reset clap_times



except KeyboardInterrupt:
    print("Exited gracefully")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
