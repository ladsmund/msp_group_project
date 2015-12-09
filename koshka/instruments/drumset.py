from sampler import Sampler


class Drumset(Sampler):
    name = 'Drumset'

    SAMPLEPATH = "samples/drumset/"
    KICK = SAMPLEPATH + "kick.wav"
    SNARE = SAMPLEPATH + "snare.wav"
    TOM1 = SAMPLEPATH + "tom1.wav"
    TOM2 = SAMPLEPATH + "tom2.wav"
    HIHAT = SAMPLEPATH + "hihat.wav"
    CRASH = SAMPLEPATH + "crash.wav"
    RIDE = SAMPLEPATH + "ride.wav"

    def __init__(self,
                 kick=KICK,
                 snare=SNARE,
                 tom1=TOM1,
                 tom2=TOM2,
                 hihat=HIHAT,
                 crash=CRASH,
                 ride=RIDE):

        self.kick_file = kick
        self.snare_file = snare
        self.tom1_file = tom1
        self.tom2_file = tom2
        self.hihat_file = hihat
        self.crash_file = crash
        self.ride_file = ride

        drumset_files = [self.kick_file, self.snare_file, self.tom1_file, self.tom2_file, \
                         self.hihat_file, self.crash_file, self.ride_file]

        Sampler.__init__(self, drumset_files)



        self.kick = self[0]
        self.snare = self[1]
        self.tom1 = self[2]
        self.tom2 = self[3]
        self.hihat = self[4]
        self.crash = self[5]
        self.ride = self[6]


    def play_all(self):
        for sample in self.sub_samples.itervalues():
            sample.on(0)

    def stop_all(self):
        for sample in self.sub_samples.itervalues():
            sample.off()
