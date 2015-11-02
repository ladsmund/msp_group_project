#!/usr/bin/python

import sys
import signal

from dac import DAC

from sequencer import Sequencer

if __name__ == "__main__":

    sequencer = Sequencer()
    sequencer.load(sys.argv[1])

    dac = DAC(sequencer.buffersize)

    dac.connect(sequencer.callback)
    dac.start()
   
    key = None
    try:
        while key != 'q':
            sys.stdout.write('>')
            key = sys.stdin.readline().strip()
            if key == 'p':
                sequencer.play()
            elif key == 's':
                sequencer.stop()
    except KeyboardInterrupt:
        pass

    sequencer.stop()

    dac.stop()


    exit()

   
