import sys


def cli(sequencer):
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
