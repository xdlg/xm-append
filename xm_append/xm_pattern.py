from xm_pattern_header import XmPatternHeader
from xm_pattern_packed_data import XmPatternPackedData


class XmPattern:
    def from_binary_data(self, data, number_of_channels):
        self.header = XmPatternHeader()
        offset = self.header.from_binary_data(data)

        self.packed_data = XmPatternPackedData()
        if self.header.packed_data_size > 0:
            offset += self.packed_data.from_binary_data(data[offset:],
                self.header.number_of_rows, number_of_channels)

        return offset

    def to_binary_data(self):
        data = bytearray()
        data.extend(self.header.to_binary_data())
        data.extend(self.packed_data.to_binary_data())
        return data

    def add_empty_channels(self, number_of_channels):
        self.header.add_empty_channels(number_of_channels)
        self.packed_data.add_empty_channels(number_of_channels)

    def shift_all_instruments(self, shift):
        self.packed_data.shift_all_instruments(shift)

    def __str__(self):
        s = ''
        s += str(self.header)
        s += '\n'
        s += str(self.packed_data)
        s += '\n'
        return s
