from time import sleep
from dac import DAC
from mixer import Mixer
from oscilator import Oscilator

STEP_SLEEP_INTERVAL = 0.2
BUFFER_SIZE = 2 ** 10

if __name__ == "__main__":

    dac = DAC(BUFFER_SIZE)

    mixer = Mixer()
    mixer.setVolume(0)

    dac.connect(mixer.callback)
    dac.start()

    osc = Oscilator(dac.getSamplerate(), dac.getBufferSize())
    osc.start()
    mixer.addDevice(osc)

    mixer.setVolume(.8)

    for frequency in range(100,1000,10):
        print frequency
        osc.setFreq(frequency)
        sleep(STEP_SLEEP_INTERVAL)


