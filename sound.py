#!/usr/bin/env python3

from copy import deepcopy
import sounddevice as sd

class Sound:
    def __init__(self):
        sd.default.samplerate = 44100  #44.1kHz
        sd.default.channels = 1
        return

    def StartRecording(self, seconds):
        # Idea behind this is we can background the recording of new
        # recordings while we process the last one
        self.__new_recording = sd.rec(int(seconds * sd.default.samplerate))
        return
    
    def Recording(self):
        sd.wait()  # Wait for current recording to be done
        self.__recording = deepcopy(self.__new_recording)
        return self.__recording

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    s = Sound()
    print("Recording Start")
    s.StartRecording(5)
    rec = s.Recording()
    print("Recording Finished")
    plt.plot(rec)
    plt.show()
