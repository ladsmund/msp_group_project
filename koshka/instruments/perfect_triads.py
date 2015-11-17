from mixer import Mixer
from scalesynth import MonophonicScaleSynth
from sinesynth import SineSynth


class PerfectTriads(Mixer):
    def __init__(self, samplerate, bufferSize, scale):
        Mixer.__init__(self)

        self.instrument01 = MonophonicScaleSynth(samplerate, bufferSize, scale)
        self.instrument02 = SineSynth(samplerate, bufferSize)
        self.instrument03 = SineSynth(samplerate, bufferSize)

        self.add_device(self.instrument01)
        self.add_device(self.instrument02)
        self.add_device(self.instrument03)

    def set_tone(self, tone):
        self.instrument01.set_tone(tone)
        base_frequency = self.instrument01.frequency
        self.instrument02.setFreq(base_frequency * 5. / 4)
        self.instrument03.setFreq(base_frequency * 3. / 2)

    def trigger(self, note=1, length=.1):
        self.instrument01.trigger(note, length)
        self.instrument02.trigger(note, length)
        self.instrument03.trigger(note, length)
