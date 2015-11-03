#!/usr/bin/python

import sys
import signal

from dac import DAC

from sequencer import Sequencer

from gui.main_window import MainWindow
from Tkinter import Tk

if __name__ == "__main__":

    sequencer = Sequencer()
    sequencer.load(sys.argv[1])

    dac = DAC(sequencer.buffersize)

    dac.connect(sequencer.callback)
    dac.start()
  
    root = Tk()
    window = MainWindow(root, sequencer)
    root.mainloop()
 
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

   
