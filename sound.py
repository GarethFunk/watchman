#!/usr/bin/env python3

from copy import deepcopy
from numpy import fft
from scipy import signal
import sounddevice as sd

class Sound:
    def __init__(self):
        self.__samplerate = 44100  #44.1kHz
        sd.default.samplerate = self.__samplerate
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

    def Filter(self, rec):
        rec = rec.reshape(rec.size)  # 1D arrays play nicely
        # From manual inspection of the desired signal, there is a 
        # strong frequency components at ~490, ~1480, ~2470, and ~3460Hz
        # the strongest one is ~3460Hz so let's bandpass filter for that
        sos = signal.butter(10, [3400, 3500], btype="bandpass", output="sos", fs=self.__samplerate)
        filtered = signal.sosfilt(sos, rec)
        return filtered
    
    def Threshold(self, rec):
        rec = rec.reshape(rec.size)  # 1D arrays play nicely
        # Half the mean. Heursitic. 
        threshold = np.mean(np.absolute(rec))/2.0
        return threshold

    def Envelope(self, filtered, threshold):
        # Now that we have the frequency content, we need to match against
        # the known time-domain beep pattern beep.beep....beep.beep....
        analytic_signal = signal.hilbert(filtered)
        amplitude_envelope = np.absolute(analytic_signal)
        # Tidy up the envelope by thresholding on mean of input signal
        amplitude_envelope[amplitude_envelope < threshold] = 0
        amplitude_envelope[amplitude_envelope >= threshold] = threshold
        return amplitude_envelope

    def PatternMatched(self, amplitude_envelope):
        match = False
        # Need to translate the envelope signal into an on-time off-time on-time 
        # sort of format
        peaks, _ = signal.find_peaks(amplitude_envelope)
        widths, _, left, right = signal.peak_widths(amplitude_envelope, peaks)
        # Translate to seconds
        widths = [x/self.__samplerate for x in widths]
        left = [x/self.__samplerate for x in left]
        right = [x/self.__samplerate for x in right]
        # discard any widths < 0.1 seconds as noise
        pattern = [x for x in zip(widths, left, right) if x[0] > 0.1]
        # Patter we're looking for in a pure sense is 0.25 on 0.25 off 0.25 on 
        # however we under-read ontime and over-read offtime
        # we need at least two widths
        if len(pattern) < 2:
            match = False
        else:
            for i in range(len(pattern)-1):
                ontime1 = pattern[i][0]
                if ontime1 > 0.2 and ontime1 < 0.3:
                    # On time is correct - this is first valid peak
                    offtime = pattern[i+1][1] - pattern[i][2]
                    if offtime > 0.2 and offtime < 0.3:
                        # off time is correct
                        ontime2 = pattern[i+1][0]
                        if ontime2 > 0.2 and ontime2 < 0.3:
                            # On-off-on pattern found!
                            match = True
                            break
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
        return match


if __name__ == "__main__":
    import numpy as np
    from scipy import signal
    import matplotlib.pyplot as plt
    s = Sound()
    print("Recording Start")
    s.StartRecording(5)
    rec = s.Recording()
    print("Recording Finished")
    n = rec.shape[0]
    sp = fft.fft(rec, axis=0)
    freq_positive = fft.fftfreq(n, 1.0/44100.0)[1:int(n/2)]
    sp_positive = np.absolute(sp)[1:int(n/2)]
    peaks = signal.find_peaks(sp_positive.reshape(sp_positive.size), height=5.0, distance=1000)
    print([freq_positive[x] for x in peaks[0]])
    plt.plot(rec)
    filt = s.Filter(rec)
    env = s.Envelope(filt, s.Threshold(rec))
    plt.plot(filt)
    plt.plot(env)
    plt.show()
    print(s.PatternMatched(env))
