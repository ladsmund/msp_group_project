from src.mixer import Mixer
import time
from exceptions import Exception
import threading

from src.dac import DAC

class Sequencer(Mixer):
    DEFAULT_SPEED = 120

    def __init__(self,
                 buffer_size=512,
                 sample_rate=44100,
                 speed=DEFAULT_SPEED,
                 tick_resolution=1024):
        Mixer.__init__(self)
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size

        self.start_time = 0
        self.speed = speed
        self.tick_resolution = tick_resolution

        self.running = False
        self.loop = False
        self._worker_threads = []
        self._active_threads = 0

        self.dac = DAC(self.buffer_size, self.sample_rate)
        self.dac.connect(self.callback)
        self.dac.start()

    def set_speed(self, speed):
        self.speed = speed

    def _get_time(self):
        return self.speed * (time.time() - self.start_time) / 60

    def _worker(self, score):
        worker_time = 0
        self._active_threads += 1
        while self.running:
            for (instrument, tone, on, wait_time) in score:
                if not self.running:
                    break

                worker_time += wait_time
                while (worker_time > self._get_time()):
                    time.sleep(0.5)

                if on:
                    self.channels[instrument].device.on(tone)
                else:
                    self.channels[instrument].device.off(tone)
            if not self.loop:
                break

        self._active_threads -= 1

    def play(self, score=[], block=False):

        if not self.running:

            self.running = True

            thread = threading.Thread(target=self._worker, args=(score,))
            self._worker_threads.append(thread)

            self.start_time = time.time()
            [t.start() for t in self._worker_threads]
        else:
            raise Exception('Already playing')

        if block:
            while self._active_threads > 0:
                time.sleep(.1)
            self.stop()

    def stop(self):
        self.running = False
        print "stopping"
        [t.join() for t in self._worker_threads]
        self._worker_threads = []
