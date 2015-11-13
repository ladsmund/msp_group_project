import time

from oscilator import Oscilator


class ScaleSynth(Oscilator):

    def __init__(self, samplerate, bufferSize, scale):
        self.scale = scale 
        Oscilator.__init__(self, samplerate, bufferSize)
        self.on = False
        self.length = 0
        self.trigger_start = 0
        self.start()

    def set_tone(self, tone):
        frequency = self.scale.get_interval_frequency(tone)
        self.setFreq(frequency)

    def trigger(self, note=1, length =.1):
        self.on = True
        self.length = length
        self.trigger_start = time.time()

    def callback(self, in_data, frame_count, time_info, status):
        output_buffer = Oscilator.callback(self, in_data, frame_count, time_info, status)

        if time.time() - self.trigger_start > self.length:
            self.on = False

        if not self.on:
            output_buffer *= 0

        return output_buffer


    def __str__(self):
        string = "SineSynth\n  Frequency: %0.1f"%self.frequency
        return string

    # def __init__(self, frequency):
    #     self.oscilator = Oscilator
    #     pass

    # def start(self):
    #     pass

    # def stop(self):
    #     pass

    # def callback(self, in_data, frame_count, time_info, status):
    #     pass




