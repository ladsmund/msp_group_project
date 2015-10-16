from time import sleep
from dac import DAC
from mixer import Mixer
from oscilator import Oscilator

STEP_SLEEP_INTERVAL = 0.2
BUFFER_SIZE = 2 ** 10

if __name__ == "__main__":

    oscilator_list = []
    frequencies = [200, 300, 400, 1000, 4000, 4090]
    gains = [.1, .1, .1, .1, .01, .01]
    rythms = []
    rythms.append([1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0])
    rythms.append([0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1])
    rythms.append([1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1])
    rythms.append([0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0])
    rythms.append([1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1])
    rythms.append([0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0])

    dac = DAC(BUFFER_SIZE)

    mixer = Mixer()
    mixer.setVolume(0)

    dac.connect(mixer.callback)
    dac.start()

    mixer.setVolume(.8)

    for i in range(0, len(frequencies)):
        f = frequencies[i]
        g = gains[i]
        osc = Oscilator(dac.getSamplerate(), dac.getBufferSize())
        osc.setFreq(f, g)
        mixer.addDevice(osc)
        oscilator_list.append(osc)

    print len(oscilator_list)

    i = 0
    while True:

        oscilator_index = 0
        for j in range(0, len(oscilator_list)):
            rythm = rythms[j]
            osc = oscilator_list[j]
            if rythm[i]:
                osc.start()
            else:
                osc.stop()

        sleep(STEP_SLEEP_INTERVAL)

        i += 1
        i %= 8
