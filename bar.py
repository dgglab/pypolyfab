from device_geo import Device, Feature


class Bar(Device):
    '''
    Bar creates a simple two-terimnal bar of a given width and length
    with contacts on both ends
    '''

    def __init__(self, bar_length, bar_width, pad=0.1):
        Device.__init__(self)
        self.bar_length = bar_length
        self.bar_width = bar_width
        self.pad = pad
        self.generate_body()
        self.add_ohmics()
        self.heal()

    def generate_body(self):
        L = self.bar_length
        W = self.bar_width

        ps = [(-W/2.0,  L/2.0),
              (W/2.0,  L/2.0),
              (W/2.0, -L/2.0),
              (-W/2.0, -L/2.0)]

        body = Feature(ps)
        self.register_feature(body, 0)

    def add_ohmics(self):
        L = self.bar_length
        W = self.bar_width
        pad = self.pad

        # Bottom ohmic
        ps = [(-W/2.0 - pad, -L/2.0 + pad),
              (W/2.0 + pad, -L/2.0 + pad),
              (W/2.0 + pad, -L/2.0 - pad),
              (-W/2.0 - pad, -L/2.0 - pad)]

        ohm0 = Feature(ps)
        self.register_feature(ohm0, 1)

        # Top ohmic
        ps = [(-W/2.0 - pad, L/2.0 + pad),
              (W/2.0 + pad, L/2.0 + pad),
              (W/2.0 + pad, L/2.0 - pad),
              (-W/2.0 - pad, L/2.0 - pad)]

        ohm1 = Feature(ps)
        self.register_feature(ohm1, 1)
