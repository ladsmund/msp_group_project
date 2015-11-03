import pyaudio
import numpy as np


class DAC():
    def __init__(self, bufferSize=1024, rate=48000, depth=16, channels=1):
        (self.paFormat, self.npFormat) = self._depth2format(depth)
        self.npFormatVal = np.iinfo(self.npFormat)
        self.rate = rate
        self.bufferSize = bufferSize
        self.channels = channels
        self.callback = None
        self.silenceBuffer = np.zeros(self.bufferSize, dtype=self.npFormat)

        '''Initialize pyAudio stream'''
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format=self.paFormat,
                                   channels=self.channels,
                                   rate=self.rate,
                                   frames_per_buffer=self.bufferSize,
                                   output=True,
                                   stream_callback=self._callback)

    def __del__(self):
        self.stop()
        self.stream.close()
        self.py.terminate()

    def getBufferSize(self):
        return self.bufferSize

    def getSamplerate(self):
        return self.rate

    def _callback(self, in_data, frame_count, time_info, status):
        out_array = self.callback(in_data, frame_count, time_info, status)

        if out_array is not None and len(out_array) == self.bufferSize:
            '''Convert the data format for the audio interface'''

            out_scale = self.npFormatVal.max * out_array

            '''Limit withing depth'''
            out_limit = np.clip(out_scale, self.npFormatVal.min, self.npFormatVal.max)

            out_array_fmt = np.array(out_limit, dtype=self.npFormat)

        else:
            out_array_fmt = self.silenceBuffer

        return (out_array_fmt.tostring(), pyaudio.paContinue)

    def connect(self, callback):
        self.callback = callback

    def start(self):
        if self.callback is not None:
            self.stream.start_stream()

    def stop(self):
        self.stream.stop_stream()

    def _depth2format(self, depth):
        if depth == 16:
            return (pyaudio.paInt16, np.int16)
        elif depth == 24:
            raise Exception("Audio depth not supported")
        else:
            raise Exception("Audio depth not supported")
