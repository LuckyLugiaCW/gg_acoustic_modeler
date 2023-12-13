from tkinter import filedialog as fd
from pydub import AudioSegment
from scipy.io import wavfile
from scipy.signal import welch
import matplotlib.pyplot as plt
import numpy as np


class Model:
    def __init__(self, filepath):
        self.imported = False
        self.filepath = filepath
        self.length = ''
        self.time = None
        self.max_res = None
        self.data_rt60 = None
        self.avg_diff = None
        self.plot_name = ["rt60_low.png", "rt60_mid.png", "rt60_high.png"]
        self.plot_color = ["red", "green", "blue"]
        self.plot_shown = 0
        self.plot_combined = False

    def import_wav(self):
        """
        Import the audio and assign values
        :return:
        """

        filetypes = (
            ('Wave', '*.wav'),
            ('MP3 - requires conversion', '*.mp3'),
            ('All files', '*.*')
        )

        filepath = fd.askopenfilename(
            title='Choose file to import',
            initialdir='/',
            filetypes=filetypes
        )

        wav = AudioSegment.empty()

        if filepath.endswith('.wav'):
            wav = AudioSegment.from_file(filepath, format="wav")
        elif filepath.endswith('.mp3'):
            wav = AudioSegment.from_mp3(filepath)
        else:
            raise ValueError(f'Unsupported file type: {filepath}')

        self.filepath = filepath

        wav.tags = None
        mono_wav = wav.set_channels(channels=1)
        mono_wav.export("acoustics.wav", format="wav")

        sample_rate, data = wavfile.read("acoustics.wav")

        self.length = round(data.shape[0] / sample_rate, 2)

        frequencies, power = welch(data, sample_rate, nperseg=4096)
        self.max_res = round(frequencies[np.argmax(power)])

        plt.plot(np.linspace(0., self.length, data.shape[0]), data)
        plt.title("Waveform")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.savefig("waveform.png")
        plt.clf()

        spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024,
                                              cmap=plt.get_cmap('autumn_r'))
        cbar = plt.colorbar(im)
        plt.title("Spectrogram")
        plt.xlabel("Time (s)")
        plt.ylabel("Frequency (Hz)")
        cbar.set_label("Intensity (dB)")
        plt.grid(color="red")
        plt.savefig("spec.png")
        plt.clf()

        self.data_rt60 = 0.0

        for x in range(0, 2):
            for y in range(0, 3):
                self.data_rt60 += self.plot_rt60(x, y, spectrum, freqs, t, self.plot_color[y])

                if x == 0:
                    plt.savefig(self.plot_name[y])
                    plt.clf()

            if x == 1:
                plt.savefig("rt60_combined.png")
                plt.clf()

        self.avg_diff = (self.data_rt60 / 6) - 0.5

    @staticmethod
    def plot_rt60(x, y, spectrum, freqs, t, color):
        def find_nearest_value(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return array[idx]

        def_freq = (1000 * pow(5, y - 1))
        target_freq = def_freq
        for target_freq in freqs:
            if target_freq > def_freq:
                break

        data_db = (10 * np.log10(spectrum[np.where(freqs == target_freq)]))[0]

        if x == 0 or y == 0:
            plt.figure()
            plt.grid()

        plt.plot(t, data_db, linewidth=1, alpha=0.7, color=color)
        plt.title("RT60")
        plt.xlabel("Time (s)")
        plt.ylabel("Power (dB)")

        max_index = np.argmax(data_db)
        max_value = data_db[max_index]
        plt.plot(t[max_index], data_db[max_index], 'k^')

        data_slice = data_db[max_index:]

        max_less_5_value = find_nearest_value(data_slice, max_value - 5)
        max_less_5_index = np.where(data_db == max_less_5_value)
        plt.plot(t[max_less_5_index], data_db[max_less_5_index], 'ks')

        max_less_25_value = find_nearest_value(data_slice, max_value - 25)
        max_less_25_index = np.where(data_db == max_less_5_value)
        plt.plot(t[max_less_5_index], data_db[max_less_5_index], 'kp')

        rt20 = t[max_less_5_index] - t[max_less_25_index]
        rt60 = 3 * rt20
        return float(rt60)

