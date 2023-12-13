# Acoustic Modeler

Allows the user to import sound files and displays information about its waveform, frequencies, and resonance. If you want to observe how different properties of sound interact, this is your module.

---

## Buttons

### Import
Opens a prompt that allows the user to select a file. Currently, only wav and mp3 files are accepted.

### Low/Mid/High
Changes the RT60 graph between low (~200 Hz), mid (~1000 Hz), and high (~5000 Hz) frequencies.

### Split/Merged
Changes whether the RT60 graphs display separately or together.

---

## Graphs

### Waveform
The amplitude of the audio over the file's duration.

### Spectrogram
The intensity of different frequencies in the audio over the file's duration.

### RT60
The intensity of the audio at a certain frequency over the file's duration.

Target frequency can be toggled (see Low/Mid/High), or all three options can be displayed at once (see Split/Merged).

---

## Other Outputs

### Duration
Duration of the audio file in seconds.

### Resonance
Frequency of the highest amplitude in Hertz.

### Difference (currently broken)
Difference between average RT60 and 0.5 seconds.
