import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

def plot_psd(audio_data, sample_rate):
    plt.figure(figsize=(10, 6))
    plt.psd(audio_data, NFFT=1024, Fs=sample_rate)
    plt.title("Power Spectral Density (PSD)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("PSD [V**2/Hz]")
    plt.xlim(0, 20000)  # focusing on the lower frequency range where claps typically are
    plt.show()

def analyze_clap(file_path):
    # Read the wave file
    sample_rate, audio_data = read(file_path)

    # Convert to mono if the audio file has 2 channels
    if len(audio_data.shape) == 2:
        audio_data = np.mean(audio_data, axis=1, dtype=int)

    plot_psd(audio_data, sample_rate)

if __name__ == "__main__":
    file_path = "data/clap43.wav"
    analyze_clap(file_path)
