import sys

class XmHeader:
    def from_binary_data(self, data):
        self.id = data[0:17]
        self.module_name = data[17:37]
        self.filler = data[37]
        self.tracker_name = data[38:58]
        self.version_number = data[58:60]
        self.length = int.from_bytes(data[60:64], sys.byteorder)
        self.song_length = int.from_bytes(data[64:66], sys.byteorder)
        self.song_restart_position = int.from_bytes(data[66:68], sys.byteorder)
        self.number_of_channels = int.from_bytes(data[68:70], sys.byteorder)
        self.number_of_patterns = int.from_bytes(data[70:72], sys.byteorder)
        self.number_of_instruments = int.from_bytes(data[72:74], sys.byteorder)
        self.flags = data[74:76]
        self.default_tempo = int.from_bytes(data[76:78], sys.byteorder)
        self.default_bpm = int.from_bytes(data[78:80], sys.byteorder)
        self.pattern_order = data[80:336]
        return 336

    def to_binary_data(self):
        data = bytearray()
        data.extend(self.id)
        data.extend(self.module_name)
        data.extend(self.filler.to_bytes(1, sys.byteorder))
        data.extend(self.tracker_name)
        data.extend(self.version_number)
        data.extend(self.length.to_bytes(4, sys.byteorder))
        data.extend(self.song_length.to_bytes(2, sys.byteorder))
        data.extend(self.song_restart_position.to_bytes(2, sys.byteorder))
        data.extend(self.number_of_channels.to_bytes(2, sys.byteorder))
        data.extend(self.number_of_patterns.to_bytes(2, sys.byteorder))
        data.extend(self.number_of_instruments.to_bytes(2, sys.byteorder))
        data.extend(self.flags)
        data.extend(self.default_tempo.to_bytes(2, sys.byteorder))
        data.extend(self.default_bpm.to_bytes(2, sys.byteorder))
        data.extend(self.pattern_order)
        return data

    def get_relevant_pattern_order(self):
        return bytearray(self.pattern_order[0:self.song_length])

    def __str__(self):
        s = ''
        s += 'XM header\n'
        s += '---------\n'
        s += 'ID: {}\n'.format(self.id)
        s += 'Module name: {}\n'.format(self.module_name)
        s += 'Filler: {}\n'.format(self.filler)
        s += 'Tracker name: {}\n'.format(self.tracker_name)
        s += 'Version number: {}\n'.format(self.version_number)
        s += 'Header length: {}\n'.format(self.length)
        s += 'Song length: {}\n'.format(self.song_length)
        s += 'Song restart position: {}\n'.format(self.song_restart_position)
        s += 'Number of channels: {}\n'.format(self.number_of_channels)
        s += 'Number of patterns: {}\n'.format(self.number_of_patterns)
        s += 'Number of instruments: {}\n'.format(self.number_of_instruments)
        s += 'Flags: {}\n'.format(self.flags)
        s += 'Default tempo: {}\n'.format(self.default_tempo)
        s += 'Default BPM: {}\n'.format(self.default_bpm)
        s += 'Pattern order: ' + ', '.join('{:02x}'.format(x) for x in self.pattern_order)
        s += '\n'
        return s

