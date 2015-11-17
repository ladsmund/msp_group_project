#!/usr/bin/python

from pythag_series import PythagSeries


class PythagMode:
    def __init__(self, mode, frequency):

        self.name = mode.lower()
        self.freq = frequency

        # An empty string does not transform to a different mode
        if self.name == "":
            self.tonic = 1
            self.name = "ionian"
        elif self.name == "dorian":
            self.tonic = 2
        elif self.name == "phrygian":
            self.tonic = 3
        elif self.name == "lydian":
            self.tonic = 4
        elif self.name == "mixolydian":
            self.tonic = 5
        elif self.name == "aeolian":
            self.tonic = 6
        elif self.name == "locrian":
            self.tonic = 7
        elif self.name == "ionian":
            self.tonic = 8
        else:
            print("Invalid mode chosen.")
            exit(1)

        mode_freqs = PythagSeries(self.freq).get_natural_scale()

        # Modify the frequency list to the mode for which a string was given
        # Basically, "roll up" to the appropriate mode by multiplying the tonic by 2
        i = self.tonic
        while i > 1:
            mode_freqs.pop(0)
            mode_freqs.append(mode_freqs[0] * 2)
            i = i - 1

        self.freqs = mode_freqs

        mode_freqs_alt = PythagSeries(mode_freqs[0]).get_natural_scale()

        self.freqs_alt = mode_freqs_alt
