import sys


class XmSampleHeader:
    def from_binary_data(self, data):
        self.sample_length = int.from_bytes(data[0:4], sys.byteorder)
        self.sample_loop_start = int.from_bytes(data[4:8], sys.byteorder)
        self.sample_loop_length = int.from_bytes(data[8:12], sys.byteorder)
        self.volume = data[12]
        self.finetune = data[13]
        self.sample_type = data[14]
        self.panning = data[15]
        self.relative_note_number = data[16]
        self.reserved = data[17]
        self.sample_name = data[18:40]
        return 40

    def to_binary_data(self):
        data = bytearray()
        data.extend(self.sample_length.to_bytes(4, sys.byteorder))
        data.extend(self.sample_loop_start.to_bytes(4, sys.byteorder))
        data.extend(self.sample_loop_length.to_bytes(4, sys.byteorder))
        data.extend(self.volume.to_bytes(1, sys.byteorder))
        data.extend(self.finetune.to_bytes(1, sys.byteorder))
        data.extend(self.sample_type.to_bytes(1, sys.byteorder))
        data.extend(self.panning.to_bytes(1, sys.byteorder))
        data.extend(self.relative_note_number.to_bytes(1, sys.byteorder))
        data.extend(self.reserved.to_bytes(1, sys.byteorder))
        data.extend(self.sample_name)
        return data

    def __str__(self):
        s = ''
        s += 'XM sample header\n'
        s += '----------------\n'
        s += 'Sample length: {}\n'.format(self.sample_length)
        s += 'Sample loop start: {}\n'.format(self.sample_loop_start)
        s += 'Sample loop length: {}\n'.format(self.sample_loop_length)
        s += 'Volume: {}\n'.format(self.volume)
        s += 'Finetune: {}\n'.format(self.finetune)
        s += 'Sample type: {}\n'.format(self.sample_type)
        s += 'Panning: {}\n'.format(self.panning)
        s += 'Relative note number: {}\n'.format(self.relative_note_number)
        s += 'Reserved: {}\n'.format(self.reserved)
        s += 'Sample name: {}\n'.format(self.sample_name)
        return s
