#!/usr/bin/env python3

import sounddevice as sd
from scipy.io.wavfile import write
import os

print('Go')
fs = 44100  # Sample rate
seconds = 30  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
write('../pretest.wav', fs, myrecording)  # Save as WAV file

dir = os.path.dirname(os.path.realpath(__file__))
os.system('ffmpeg -i {0}/pretest.wav -ar 44100 -ac 1 -acodec pcm_s16le {1}/test.wav -y'.format(dir,dir))
print('Done Recording...Using Record.py')
