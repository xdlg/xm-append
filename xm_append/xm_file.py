from xm_header import XmHeader
from xm_pattern import XmPattern
from xm_instrument import XmInstrument


class XmFile:
    def from_file(self, file_name):
        with open(file_name, 'rb') as file:
            file_data = file.read()
            offset = 0

            self.header = XmHeader()
            offset = self.header.from_binary_data(file_data[offset:])

            self.patterns = []
            for i in range(self.header.number_of_patterns):
                pattern = XmPattern()
                offset += pattern.from_binary_data(file_data[offset:],
                    self.header.number_of_channels)
                self.patterns.append(pattern)

            self.instruments = []
            for i in range(self.header.number_of_instruments):
                instrument = XmInstrument()
                offset += instrument.from_binary_data(file_data[offset:])
                self.instruments.append(instrument)

    def to_file(self, file_name):
        file_data = self.header.to_binary_data()

        for pattern in self.patterns:
            file_data.extend(pattern.to_binary_data())

        for instrument in self.instruments:
            file_data.extend(instrument.to_binary_data())

        with open(file_name, 'wb') as file:
            file.write(file_data)

    def remove_empty_instruments(self):
        empty_instruments = []
        for instrument in self.instruments:
            if instrument.is_empty():
                empty_instruments.append(instrument)

        for empty_instrument in empty_instruments:
            empty_instrument_index = self.instruments.index(empty_instrument) + 1
            for pattern in self.patterns:
                for row in pattern.packed_data.rows:
                    for note in row.notes:
                        if note.instrument is not None and note.instrument > empty_instrument_index:
                            note.instrument -= 1
            self.instruments.remove(empty_instrument)
            self.header.number_of_instruments -= 1

    def rename_instruments_by_index(self):
        for instrument in self.instruments:
            instrument_index = self.instruments.index(instrument) + 1
            new_name = str(instrument_index).encode('utf-8')
            empty_bytes = bytes(len(instrument.header.instrument_name) - len(new_name))
            new_name += empty_bytes
            instrument.header.instrument_name = new_name

    def add_empty_channels(self, number_of_channels):
        for pattern in self.patterns:
            pattern.add_empty_channels(number_of_channels)
        self.header.number_of_channels += number_of_channels

    def append(self, other_xm_file):
        largest_number_of_channels = max(
            self.header.number_of_channels, other_xm_file.header.number_of_channels)

        if self.header.number_of_channels < largest_number_of_channels:
            number_of_channels_to_add = largest_number_of_channels - self.header.number_of_channels
            self.add_empty_channels(number_of_channels_to_add)
        elif other_xm_file.header.number_of_channels < largest_number_of_channels:
            number_of_channels_to_add = largest_number_of_channels - other_xm_file.header.number_of_channels
            other_xm_file.add_empty_channels(number_of_channels_to_add)
        self.header.number_of_channels = largest_number_of_channels

        old_number_of_patterns = self.header.number_of_patterns
        self.header.number_of_patterns += other_xm_file.header.number_of_patterns
        self.patterns.extend(other_xm_file.patterns)
        for i in range (old_number_of_patterns, self.header.number_of_patterns):
            self.patterns[i].shift_all_instruments(self.header.number_of_instruments)

        this_pattern_order = self.header.get_relevant_pattern_order()
        other_pattern_order = other_xm_file.header.get_relevant_pattern_order()
        for i in range(len(other_pattern_order)):
            other_pattern_order[i] += old_number_of_patterns
        padding = bytearray(len(self.header.pattern_order) - len(this_pattern_order) - len(other_pattern_order))
        this_pattern_order.extend(other_pattern_order)
        this_pattern_order.extend(padding)
        self.header.pattern_order = this_pattern_order
        self.header.song_length += other_xm_file.header.song_length

        self.header.number_of_instruments += other_xm_file.header.number_of_instruments
        for instrument in other_xm_file.instruments:
            self.instruments.append(instrument)

    def __str__(self):
        s = ''
        s += str(self.header)
        s += '\n'
        s += '\n'.join('{}'.format(pattern) for pattern in self.patterns)
        s += '\n'
        s += '\n'.join('{}'.format(instrument) for instrument in self.instruments)
        return s
