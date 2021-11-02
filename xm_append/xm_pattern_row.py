from xm_note import XmNote


class XmPatternRow:
    def from_binary_data(self, data, number_of_channels):
        offset = 0
        self.notes = []

        for i in range(number_of_channels):
            note = XmNote()
            offset += note.from_binary_data(data[offset:])
            self.notes.append(note)

        return offset

    def to_binary_data(self):
        data = bytearray()
        for note in self.notes:
            data.extend(note.to_binary_data())
        return data

    def add_empty_channels(self, number_of_channels):
        for i in range (number_of_channels):
            self.notes.append(XmNote())

    def shift_all_instruments(self, shift):
        for note in self.notes:
            if (note.instrument is not None
                and (note.instrument + shift) >= 0
                and (note.instrument + shift) <= 255):
                note.instrument += shift

    def __str__(self):
        return ' - '.join('{}'.format(note) for note in self.notes)
