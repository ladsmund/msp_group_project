from sampler import PolyphonicSampler

class Drumset(PolyphonicSampler):

    SAMPLEPATH = "samples/drumset/"
    KICK = SAMPLEPATH + "kick.wav"
    SNARE = SAMPLEPATH + "snare.wav"
    TOM1 = SAMPLEPATH + "tom1.wav"
    TOM2 = SAMPLEPATH + "tom2.wav"
    HIHAT = SAMPLEPATH + "hihat.wav"
    CRASH = SAMPLEPATH + "crash.wav"
    RIDE = SAMPLEPATH + "ride.wav"

    def __init__(self, kick=KICK, snare=SNARE, tom1=TOM1, tom2=TOM2, \
                    hihat=HIHAT, crash=CRASH, ride=RIDE):
        self.kick =  kick
        self.snare = snare
        self.tom1 =  tom1
        self.tom2 =  tom2
        self.hihat = hihat
        self.crash = crash
        self.ride =  ride

        drumset_files = [ self.kick, self.snare, self.tom1, self.tom2,\
                            self.hihat, self.crash, self.ride ]

        PolyphonicSampler.__init__(self, drumset_files)
        
    def play_all(self):
        for sample in self.sub_samples.itervalues():
            sample.on(0)

    def stop_all(self):
        for sample in self.sub_samples.itervalues():
            sample.off()
        
