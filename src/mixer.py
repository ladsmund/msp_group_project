DEFAULT_CHANNEL_GAIN = 1.


class Channel:
    def __init__(self, device, gain=DEFAULT_CHANNEL_GAIN):
        self.gain = gain
        self.device = device
        self.mute = False

    def set_gain(self, gain):
        self.gain = gain

    def callback(self, in_data, frame_count, time_info, status):
        if self.mute:
            return 0 * self.device.callback(in_data, frame_count, time_info, status)
        else:
            return self.gain * self.device.callback(in_data, frame_count, time_info, status)


class Mixer:
    def __init__(self):
        self.channels = []
        self.volume = 1
        pass

    def setVolume(self, volume):
        self.volume = volume

    def getVolume(self):
        return self.volume

    def callback(self, in_data, frame_count, time_info, status):
        output_buffer = None
        for channel in self.channels:
            channel_buffer = channel.callback(in_data, frame_count, time_info, status)

            if output_buffer is None:
                output_buffer = channel_buffer
            else:
                output_buffer += channel_buffer

        if output_buffer is None:
            return None

        return self.volume * output_buffer

    def add_device(self, device):
        channel = Channel(device)
        self.channels.append(channel)
        return channel
