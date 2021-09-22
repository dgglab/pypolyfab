from device_geo import Device, Feature


class CHB(Device):
    '''
    CHB creates a collimating Hall bar
    '''

    def __init__(self, L, W, pad=0.1):
        Device.__init__(self)
        self.body_length = L
        self.body_width = W
        self.pad = pad
        self.apt_width = 0.3
        self.apt_bottom = .05
        self.apt_overhang = 0.5
        self.edgeslope = 0.3
        self.col_ohmic_gap = 0.2
        self.col_ohmic_offset = 0.05
        self.inj_width = 0.8
        self.inj_length = 0.6
        self.inj_separation = 2.76
        self.col_length = 0.8
        self.fractional_cover = 0.2

        self.generate_body()
        self.add_collimators()
        self.add_side_ohmics()
        self.heal()

    def generate_body(self):
        L = self.body_length
        W = self.body_width

        ps = [(-L/2.0,  W/2.0),
              (L/2.0,  W/2.0),
              (L/2.0, -W/2.0),
              (-L/2.0, -W/2.0)]

        body = Feature(ps)
        self.register_feature(body, 0, 0, 0, 0)

    def add_collimators(self):
        self.generate_collimator(-self.inj_separation /
                                 2, -self.body_width/2, 0, 1)
        self.generate_collimator(
            self.inj_separation/2, -self.body_width/2, 0, 2)
        self.generate_collimator(-self.inj_separation/2,
                                 self.body_width/2, 180, 2)
        self.generate_collimator(
            self.inj_separation/2, self.body_width/2, 180, 2)

    def add_side_ohmics(self):
        W = self.body_width
        L = self.body_length
        pad = self.pad
        Dx = -L/2 + L*self.fractional_cover - 0.5

        ps = [(-L/2-pad, -W/2-pad),
              (-L/2-pad, W/2+pad),
              (Dx, W/2+pad),
              (Dx, -W/2-pad)]

        left_ohmic = Feature(ps)
        self.register_feature(left_ohmic, 0, 0, 0, 2)

        Dx = L/2 - L*self.fractional_cover + 0.5

        ps = [(L/2+pad, W/2+pad),
              (L/2+pad, -W/2-pad),
              (Dx, -W/2-pad),
              (Dx, W/2+pad)]

        right_ohmic = Feature(ps)
        self.register_feature(right_ohmic, 0, 0, 0, 2)

    def generate_collimator(self, dx, dy, dtheta, layer):
        inj_height = self.inj_length + self.col_length + self.apt_bottom
        col_topcorner = self.apt_bottom + self.edgeslope / \
            2 * (self.inj_width-self.apt_width)
        col_bottom = self.apt_bottom + self.col_length

        # collimator body
        ps = [(self.apt_width/2, self.apt_overhang),
              (self.apt_width/2, -self.apt_bottom),
              (self.inj_width/2, -col_topcorner),
              (self.inj_width/2, -col_bottom),
              (self.apt_width/2, -col_bottom),
              (self.inj_width/2, -inj_height),
              (-self.inj_width/2, -inj_height),
              (-self.apt_width/2, -col_bottom),
              (-self.inj_width/2, -col_bottom),
              (-self.inj_width/2, -col_topcorner),
              (-self.apt_width/2, -self.apt_bottom),
              (-self.apt_width/2, self.apt_overhang)]

        injector = Feature(ps)
        self.register_feature(injector, dx, dy, dtheta, 0, origin=(0, 0))

        # ohmic around filter chamber
        pad = self.pad
        col_ohmic_W = self.inj_width + pad
        col_ohmic_L = self.col_length + pad
        apt_ohmic_W = self.apt_width + pad/2
        apt_ohmic_bottom = self.apt_bottom - pad/8
        col_ohmic_topcorner = col_topcorner - pad/2

        ps = [(-apt_ohmic_W/2, self.col_ohmic_offset),
              (apt_ohmic_W/2, self.col_ohmic_offset),
              (apt_ohmic_W/2, -apt_ohmic_bottom),
              (col_ohmic_W/2, -col_ohmic_topcorner),
              (col_ohmic_W/2, -col_ohmic_L),
              (-col_ohmic_W/2, -col_ohmic_L),
              (-col_ohmic_W/2, -col_ohmic_topcorner),
              (-apt_ohmic_W/2, -apt_ohmic_bottom)]

        ohm1 = Feature(ps)
        self.register_feature(ohm1, dx, dy, dtheta, 2, origin=(0, 0))

        # Ohmic around collimator source
        inj_ohmic_W = col_ohmic_W * 1.1
        inj_ohmic_H = self.inj_length * 0.6
        inj_ohmic_offset = self.inj_length * self.apt_bottom
        inj_base_dydx = (self.inj_width/2 - self.apt_width/2) / \
            (col_bottom - inj_height)
        inj_ohmic_dx = -inj_ohmic_H * inj_base_dydx

        ps = [(-inj_ohmic_W/2, -inj_ohmic_offset - inj_height),
              (-inj_ohmic_W/2 + inj_ohmic_dx,
               inj_ohmic_H-inj_ohmic_offset - inj_height),
              (inj_ohmic_W/2 - inj_ohmic_dx,
               inj_ohmic_H-inj_ohmic_offset - inj_height),
              (inj_ohmic_W/2, -inj_ohmic_offset - inj_height)]

        ohm2 = Feature(ps)
        self.register_feature(ohm2, dx, dy, dtheta, layer, origin=(0, 0))
