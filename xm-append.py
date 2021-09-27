#!/usr/bin/env python3

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


class XmNote:
    def __init__(self):
        self.pitch = None
        self.instrument = None
        self.volume = None
        self.effect = None
        self.effect_parameter = None

    def from_binary_data(self, data):
        offset = 0
        byte = data[offset]

        if not (data[offset] & 0x80):
            self.pitch = data[offset]
            offset += 1
            self.instrument = data[offset]
            offset += 1
            self.volume = data[offset]
            offset += 1
            self.effect = data[offset]
            offset += 1
            self.effect_parameter = data[offset]
            offset += 1

        else:
            is_pitch_encoded = data[offset] & 0x01
            is_instrument_encoded = data[offset] & 0x02
            is_volume_encoded = data[offset] & 0x04
            is_effect_encoded = data[offset] & 0x08
            is_effect_parameter_encoded = data[offset] & 0x10
            offset += 1

            if is_pitch_encoded:
                self.pitch = data[offset]
                offset += 1

            if is_instrument_encoded:
                self.instrument = data[offset]
                offset += 1

            if is_volume_encoded:
                self.volume = data[offset]
                offset += 1

            if is_effect_encoded:
                self.effect = data[offset]
                offset += 1

            if is_effect_parameter_encoded:
                self.effect_parameter = data[offset]
                offset += 1

            if not is_effect_encoded and is_effect_parameter_encoded:
                self.effect = 0

            if not is_effect_parameter_encoded and is_effect_encoded:
                self.effect_parameter = 0

        return offset

    def to_binary_data(self):
        data = bytearray()

        if ((self.pitch is not None) and (self.instrument is not None) and (self.volume is not None)
            and (self.effect is not None) and (self.effect != 0)
            and (self.effect_parameter is not None) and (self.effect_parameter != 0)):
            data.extend(self.pitch.to_bytes(1, sys.byteorder))
            data.extend(self.instrument.to_bytes(1, sys.byteorder))
            data.extend(self.volume.to_bytes(1, sys.byteorder))
            data.extend(self.effect.to_bytes(1, sys.byteorder))
            data.extend(self.effect_parameter.to_bytes(1, sys.byteorder))

        else:
            packing_byte = (0x80
                | (0x01 if self.pitch is not None else 0)
                | (0x02 if self.instrument is not None else 0)
                | (0x04 if self.volume is not None else 0)
                | (0x08 if (self.effect is not None and self.effect != 0) else 0)
                | (0x10 if (self.effect_parameter is not None and self.effect_parameter != 0) else 0))
            data.extend(packing_byte.to_bytes(1, sys.byteorder))

            if (self.pitch is not None):
                data.extend(self.pitch.to_bytes(1, sys.byteorder))
            if (self.instrument is not None):
                data.extend(self.instrument.to_bytes(1, sys.byteorder))
            if (self.volume is not None):
                data.extend(self.volume.to_bytes(1, sys.byteorder))
            if (self.effect is not None and self.effect != 0):
                data.extend(self.effect.to_bytes(1, sys.byteorder))
            if (self.effect_parameter is not None and self.effect_parameter != 0):
                data.extend(self.effect_parameter.to_bytes(1, sys.byteorder))

        return data

    def __str__(self):
        s = ''
        s += '{:02x} '.format(self.pitch) if self.pitch is not None else '/ '
        s += '{:02x} '.format(self.instrument) if self.instrument is not None else '/ '
        s += '{:02x} '.format(self.volume) if self.volume is not None else '/ '
        s += '{:02x} '.format(self.effect) if self.effect is not None else '/ '
        s += '{:02x} '.format(self.effect_parameter) if self.effect_parameter is not None else '/ '
        return s


class XmInstrument:
    def from_binary_data(self, data):
        self.header = XmInstrumentHeader()
        offset = self.header.from_binary_data(data)

        self.sample_headers = []
        for i in range(self.header.number_of_samples):
            sample_header = XmSampleHeader()
            offset += sample_header.from_binary_data(data[offset:])
            self.sample_headers.append(sample_header)

        self.samples = []
        for i in range(self.header.number_of_samples):
            sample = data[offset:(offset + self.sample_headers[i].sample_length)]
            offset += self.sample_headers[i].sample_length
            self.samples.append(sample)

        return offset

    def to_binary_data(self):
        data = bytearray()
        data.extend(self.header.to_binary_data())

        for sample_header in self.sample_headers:
            data.extend(sample_header.to_binary_data())

        for sample in self.samples:
            data.extend(sample)

        return data

    def is_empty(self):
        return ((self.header.number_of_samples == 0)
            or all(sample_header.sample_length == 0 for sample_header in self.sample_headers))

    def __str__(self):
        s = ''
        s += str(self.header)
        s += '\n'
        s += '\n'.join('{}'.format(sample_header) for sample_header in self.sample_headers)
        s += '\n'
        s += '\n'.join('{}'.format(sample) for sample in self.samples)
        s += '\n'
        return s


class XmInstrumentHeader:
    def from_binary_data(self, data):
        self.length = int.from_bytes(data[0:4], sys.byteorder)
        self.instrument_name = data[4:26]
        self.instrument_type = data[26]
        self.number_of_samples = int.from_bytes(data[27:29], sys.byteorder)
        offset = 29

        if self.number_of_samples > 0:
            self.sample_header_size = int.from_bytes(data[29:33], sys.byteorder)
            self.sample_number = data[33:129]
            self.volume_envelope = data[129:177]
            self.panning_envelope = data[177:225]
            self.number_of_volume_points = data[225]
            self.number_of_panning_points = data[226]
            self.volume_sustain_point = data[227]
            self.volume_loop_start_point = data[228]
            self.volume_loop_end_point = data[229]
            self.panning_sustain_point = data[230]
            self.panning_loop_start_point = data[231]
            self.panning_loop_end_point = data[232]
            self.volume_type = data[233]
            self.panning_type = data[234]
            self.vibrato_type = data[235]
            self.vibrato_sweep = data[236]
            self.vibrato_depth = data[237]
            self.vibrato_rate = data[238]
            self.volume_fadeout = int.from_bytes(data[239:241], sys.byteorder)
            offset = 241

        self.reserved = data[offset:self.length]
        return self.length

    def to_binary_data(self):
        data = bytearray()
        data.extend(self.length.to_bytes(4, sys.byteorder))
        data.extend(self.instrument_name)
        data.extend(self.instrument_type.to_bytes(1, sys.byteorder))
        data.extend(self.number_of_samples.to_bytes(2, sys.byteorder))

        if self.number_of_samples > 0:
            data.extend(self.sample_header_size.to_bytes(4, sys.byteorder))
            data.extend(self.sample_number)
            data.extend(self.volume_envelope)
            data.extend(self.panning_envelope)
            data.extend(self.number_of_volume_points.to_bytes(1, sys.byteorder))
            data.extend(self.number_of_panning_points.to_bytes(1, sys.byteorder))
            data.extend(self.volume_sustain_point.to_bytes(1, sys.byteorder))
            data.extend(self.volume_loop_start_point.to_bytes(1, sys.byteorder))
            data.extend(self.volume_loop_end_point.to_bytes(1, sys.byteorder))
            data.extend(self.panning_sustain_point.to_bytes(1, sys.byteorder))
            data.extend(self.panning_loop_start_point.to_bytes(1, sys.byteorder))
            data.extend(self.panning_loop_end_point.to_bytes(1, sys.byteorder))
            data.extend(self.volume_type.to_bytes(1, sys.byteorder))
            data.extend(self.panning_type.to_bytes(1, sys.byteorder))
            data.extend(self.vibrato_type.to_bytes(1, sys.byteorder))
            data.extend(self.vibrato_sweep.to_bytes(1, sys.byteorder))
            data.extend(self.vibrato_depth.to_bytes(1, sys.byteorder))
            data.extend(self.vibrato_rate.to_bytes(1, sys.byteorder))
            data.extend(self.volume_fadeout.to_bytes(2, sys.byteorder))

        data.extend(self.reserved)
        return data

    def __str__(self):
        s = ''
        s += 'XM instrument header\n'
        s += '--------------------\n'
        s += 'Length: {}\n'.format(self.length)
        s += 'Instrument name: {}\n'.format(self.instrument_name)
        s += 'Instrument type: {}\n'.format(self.instrument_type)
        s += 'Number of samples: {}\n'.format(self.number_of_samples)

        if self.number_of_samples > 0:
            s += 'Sample header size: {}\n'.format(self.sample_header_size)
            s += 'Sample number: {}\n'.format(self.sample_header_size)
            s += 'Volume envelope: {}\n'.format(self.volume_envelope)
            s += 'Panning envelope: {}\n'.format(self.panning_envelope)
            s += 'Number of volume points: {}\n'.format(self.number_of_volume_points)
            s += 'Number of panning points: {}\n'.format(self.number_of_panning_points)
            s += 'Volume sustain point: {}\n'.format(self.volume_sustain_point)
            s += 'Volume loop start point: {}\n'.format(self.volume_loop_start_point)
            s += 'Volume loop end point: {}\n'.format(self.volume_loop_end_point)
            s += 'Panning sustain point: {}\n'.format(self.panning_sustain_point)
            s += 'Panning loop start point: {}\n'.format(self.panning_loop_start_point)
            s += 'Panning loop end point: {}\n'.format(self.panning_loop_end_point)
            s += 'Volume type: {}\n'.format(self.volume_type)
            s += 'Panning type: {}\n'.format(self.panning_type)
            s += 'Vibrato type: {}\n'.format(self.vibrato_type)
            s += 'Vibrato sweep: {}\n'.format(self.vibrato_sweep)
            s += 'Vibrato depth: {}\n'.format(self.vibrato_depth)
            s += 'Vibrato rate: {}\n'.format(self.vibrato_rate)
            s += 'Volume fadeout: {}\n'.format(self.volume_fadeout)
            s += 'Reserved: {}\n'.format(self.reserved)

        return s


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


def main():
    file_in_1 = sys.argv[1]
    file_in_2 = sys.argv[2]
    file_out = sys.argv[3]

    xm_file_1 = XmFile()
    xm_file_1.from_file(file_in_1)
    xm_file_2 = XmFile()
    xm_file_2.from_file(file_in_2)

    xm_file_1.remove_empty_instruments()
    xm_file_1.rename_instruments_by_index()
    xm_file_2.remove_empty_instruments()
    xm_file_2.rename_instruments_by_index()
    xm_file_1.append(xm_file_2)

    xm_file_1.to_file(file_out)


if __name__ == "__main__":
    main()
