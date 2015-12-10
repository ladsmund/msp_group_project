from mixer import Mixer
from scalesynth import MonophonicScaleSynth
from sinesynth import SineSynth


class PerfectTriads(Mixer):
    name = "Perfect Triads"

    def __init__(self, samplerate, bufferSize, scale):
        Mixer.__init__(self)
        self.instrument01 = MonophonicScaleSynth(samplerate, bufferSize, scale)
        self.instrument02 = SineSynth(samplerate, bufferSize)
        self.instrument03 = SineSynth(samplerate, bufferSize)
        self.add_device(self.instrument01)
        self.add_device(self.instrument02)
        self.add_device(self.instrument03)
        self.tone = None

    def on(self, tone, time=0):
        base_frequency = self.instrument01.scale.get_frequency(tone)
        self.instrument01.on(tone, time=time)
        self.instrument02.on(base_frequency * 5. / 4, time=time)
        self.instrument03.on(base_frequency * 3. / 2, time=time)

    def off(self, tone=None, time=0):
        if tone is None or tone == self.tone:
            self.instrument01.off(time=time)
            self.instrument02.off(time=time)
            self.instrument03.off(time=time)

    def __str__(self):
        return "%s %s" % (type(self).__name__, str(self.instrument01.scale))
