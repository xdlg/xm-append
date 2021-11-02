import sys


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
