import pyaudio
import numpy as np
import time
import requests

# Constants
VOLUME_THRESHOLD = 12000
RATE = 8000
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

def detect_clap(audio_data):
    """Detects clap based on amplitude threshold."""
    return np.max(np.abs(audio_data)) > VOLUME_THRESHOLD

def compute_frequencies(audio_data):
    """Computes FFT and returns frequencies."""
    fft_data = np.fft.fft(audio_data)
    magnitude = np.abs(fft_data)
    frequencies = np.fft.fftfreq(len(fft_data), 1.0/RATE)
    return frequencies, magnitude

def is_clap_frequency(dominant_frequency):
    #Check whether the dominant frequency is within a clap's possible frequency range.
    return (800 <= dominant_frequency <= 2200) or (300 <= dominant_frequency <= 500)

last_clap_time = time.time() - DEBOUNCE_TIME
clap_times = []

try:
    while True:
        # Reading from audio input stream into data with BUFFER samples
        input_data = stream.read(BUFFER)
        audio_data = np.frombuffer(input_data, dtype=np.int16)

        current_time = time.time()

        if detect_clap(audio_data) and (current_time - last_clap_time >= DEBOUNCE_TIME):
            frequencies, magnitude = compute_frequencies(audio_data)
            dominant_frequency = abs(frequencies[np.argmax(magnitude)])

            # Check if the dominant frequency is in the clap frequency range
            if is_clap_frequency(dominant_frequency):
                print(f"Clap detected! Dominant frequency: {dominant_frequency:.2f} Hz")
                last_clap_time = current_time
                clap_times.append(current_time)
            else:
                print(f"Noise detected, {dominant_frequency:.2f} Hz ignored.")

        # Check for pattern reset
        if clap_times and (current_time - clap_times[-1] >= RESET_TIME):
            # Compute intervals between claps and print pattern
            intervals = [clap_times[i] - clap_times[i-1] for i in range(1, len(clap_times))]
            pattern = ["clap"]
            for interval in intervals:
                if interval < 0.5:
                    symbol = " - "
                elif interval < 1:
                    symbol = " _ "
                else:  # Add additional conditions if needed
                    symbol = " ? "
                pattern.append(symbol + "clap")
            pattern_str = "".join(pattern)
            print("Pattern:", pattern_str)
            if pattern_str == "clap - clap":
                light_state = not light_state
                url = "http://192.168.50.91/api/MGHLl7IZa-qnZJH9GC8DT9bEeUgnywktYFWtMR9T/groups/1/action"
                payload = {"on": light_state}
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "Insomnia/2023.5.6"
                }
                response = requests.request("PUT", url, json=payload, headers=headers)
                print(response.text)

            clap_times = []  # Reset clap_times

except KeyboardInterrupt:
    print("Exited gracefully")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
