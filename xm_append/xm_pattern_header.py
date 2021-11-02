import sys


class XmPatternHeader:
    def from_binary_data(self, data):
        self.length = int.from_bytes(data[0:4], sys.byteorder)
        self.packing_type = data[4]
        self.number_of_rows = int.from_bytes(data[5:7], sys.byteorder)
        self.packed_data_size = int.from_bytes(data[7:9], sys.byteorder)
        return 9

    def to_binary_data(self):
        data = bytearray()
        data.extend(self.length.to_bytes(4, sys.byteorder))
        data.extend(self.packing_type.to_bytes(1, sys.byteorder))
        data.extend(self.number_of_rows.to_bytes(2, sys.byteorder))
        data.extend(self.packed_data_size.to_bytes(2, sys.byteorder))
        return data

    def add_empty_channels(self, number_of_channels):
        self.packed_data_size += self.number_of_rows * number_of_channels

    def __str__(self):
        s = ''
        s += 'XM pattern header\n'
        s += '-----------------\n'
        s += 'Pattern header length: {}\n'.format(self.length)
        s += 'Packing type: {}\n'.format(self.packing_type)
        s += 'Number of rows: {}\n'.format(self.number_of_rows)
        s += 'Packed data size: {}\n'.format(self.packed_data_size)
        return s
