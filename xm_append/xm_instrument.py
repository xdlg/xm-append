from xm_instrument_header import XmInstrumentHeader
from xm_sample_header import XmSampleHeader


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
