import sys


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
