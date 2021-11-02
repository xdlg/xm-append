from xm_pattern_row import XmPatternRow


class XmPatternPackedData:
    def __init__(self):
        self.rows = []

    def from_binary_data(self, data, number_of_rows, number_of_channels):
        offset = 0

        for i in range(number_of_rows):
            row = XmPatternRow()
            offset += row.from_binary_data(data[offset:], number_of_channels)
            self.rows.append(row)

        return offset

    def to_binary_data(self):
        data = bytearray()
        for row in self.rows:
            data.extend(row.to_binary_data())
        return data

    def add_empty_channels(self, number_of_channels):
        for row in self.rows:
            row.add_empty_channels(number_of_channels)

    def shift_all_instruments(self, shift):
        for row in self.rows:
            row.shift_all_instruments(shift)

    def __str__(self):
        s = ''
        s += 'XM pattern packed data\n'
        s += '----------------------\n'
        s += '\n'.join('{}'.format(row) for row in self.rows)
        return s
