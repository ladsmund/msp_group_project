#!/usr/bin/python

import argparse
from time import sleep

from dac import DAC
from sequencers.grid_sequencer import GridSequencer

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Koshka - MSP project')

    parser.add_argument('score', type=str)
    parser.add_argument('--no_gui', type=bool, default=False, const=True,
                        nargs='?')
    parser.add_argument('-l', '--loop', type=int, default=0,
                        const=GridSequencer.INFINIT_LOOP, nargs='?')
    namespace = parser.parse_args()

    if namespace.no_gui:
        dac = DAC()
        dac.start()
        try:
            sequencer = GridSequencer(namespace.score, buffer_size=dac.bufferSize, sample_rate=dac.getSamplerate())
            dac.connect(sequencer.callback)
            sequencer.play(namespace.loop)

            while sequencer.running:
                sleep(0.1)

        finally:
            dac.stop()

    else:
        from gui.main_window import MainWindow
        window = MainWindow(namespace)

        window.mainloop()
        window = None

    exit()
