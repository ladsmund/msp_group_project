__author__ = 'mads'

import midi


class Event:
    def __init__(self, tone, time, length):
        self.tone = tone
        self.time = time
        self.length = length
        self.staff = None

    def set_time(self, time):
        self.time = time
        if self.staff:
            self.staff.update()


class Staff:
    def __init__(self, meter, scale):
        self.scale = scale
        self.meter = meter
        self.tones = []
        self.time = 0

    def reset_time(self, time=0):
        self.time = time

    def add_tone(self, tone):
        tone.staff = self
        self.tones.append(tone)
        self.update()

    def update(self):
        # self.tones.sort(key=lambda tone: tone.time)
        pass

    def get_active_tones(self, time):
        active_tones = [t for t in self.tones if self.time < t.time <= time]
        self.time = time
        return active_tones


if __name__ == "__main__":
    print "main"
    staff = Staff(8, None)
    import midi

    midi.read
    # Instantiate a MIDI Pattern (contains a list of tracks)
    pattern = midi.Pattern()
    # Instantiate a MIDI Track (contains a list of MIDI events)
    track = midi.Track()
    # Append the track to the pattern
    pattern.append(track)
    # Instantiate a MIDI note on event, append it to the track
    on = midi.NoteOnEvent(tick=0, velocity=20, pitch=midi.G_3)
    track.append(on)
    # Instantiate a MIDI note off event, append it to the track
    off = midi.NoteOffEvent(tick=100, pitch=midi.G_3)
    track.append(off)
    print off
    print track
    # del off in track
    # Add the end of track event, append it to the track
    eot = midi.EndOfTrackEvent(tick=1)
    track.append(eot)
    # Print out the pattern
    print pattern
    # Save the pattern to disk
    midi.write_midifile("example.mid", pattern)
