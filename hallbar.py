from device_geo import Device, Feature
import numpy as np


class HallBar(Device):
    '''
    Bar creates a simple two-terimnal bar of a given width and length
    with contacts on both ends
    '''

    def __init__(self, bar_width, num_contacts, contact_width, contact_length, sq_btw_contacts, inject_sq = 0, pad=0.1):
        Device.__init__(self)
        self.bar_width = bar_width
        self.num_contacts = num_contacts
        self.contact_width = contact_width
        self.contact_length = contact_length
        self.sq_btw_contacts = sq_btw_contacts
        self.inject_sq = inject_sq
        self.inject_length = inject_sq*bar_width
        self.pad = pad
        if inject_sq != 0:
            self.bar_length = bar_width*((num_contacts-1)*sq_btw_contacts + 2*inject_sq)
        else:
            self.bar_length = bar_width*((num_contacts-1)*sq_btw_contacts) + contact_width
        self.generate_body()
        self.add_ohmics()
        self.heal()

    def generate_body(self):
        L = self.bar_length
        W = self.bar_width

        ps = [(-L/2.0,  W/2.0),
              ( L/2.0,  W/2.0),
              ( L/2.0, -W/2.0),
              (-L/2.0, -W/2.0)]

        body = Feature(ps)
        self.register_feature(body, 0, 0, 0, 0)

        contact_width = self.contact_width
        contact_length = self.contact_length
        inject_length = self.inject_length

        for contact_num in range(self.num_contacts):
            offset = contact_num*self.sq_btw_contacts*self.bar_width
            ps = [(-L/2.0 + inject_length,   W/2.0 + contact_length),
                  (-L/2.0 + inject_length + contact_width,   W/2.0 + contact_length),
                  (-L/2.0 + inject_length + contact_width,  -W/2.0 - contact_length),
                  (-L/2.0 + inject_length,  -W/2.0 - contact_length)]
            
            ps = np.array(ps) + (offset, 0)
            contact = Feature(ps)
            self.register_feature(contact, 0, 0, 0, 0)

    def add_ohmics(self):
        L = self.bar_length
        W = self.bar_width
        pad = self.pad
        contact_width = self.contact_width
        contact_length = self.contact_length
        inject_length = self.inject_length

        # Hall contacts
        for contact_num in range(self.num_contacts):
            offset = contact_num*self.sq_btw_contacts*self.bar_width

            # Top contact
            ps = [(-L/2.0 + inject_length - pad,   W/2.0 + contact_length + pad),
                  (-L/2.0 + inject_length + contact_width + pad,   W/2.0 + contact_length + pad),
                  (-L/2.0 + inject_length + contact_width + pad,   W/2.0 + contact_length -pad),
                  (-L/2.0 + inject_length - pad,   W/2.0 + contact_length - pad)]
            
            ps = np.array(ps) + (offset, 0)
            ohmic = Feature(ps)
            self.register_feature(ohmic, 0, 0, 0, 1)

            # Bot contact
            ps = [(-L/2.0 + inject_length - pad,   -W/2.0 - contact_length + pad),
                  (-L/2.0 + inject_length + contact_width + pad,   -W/2.0 - contact_length + pad),
                  (-L/2.0 + inject_length + contact_width + pad,   -W/2.0 - contact_length -pad),
                  (-L/2.0 + inject_length - pad,   -W/2.0 - contact_length - pad)]
            
            ps = np.array(ps) + (offset, 0)
            ohmic = Feature(ps)
            self.register_feature(ohmic, 0, 0, 0, 1)

        # Side contacts
        if self.inject_sq != 0:
            # Left side ohmic
            ps = [(-L/2.0 - pad,  W/2.0 + pad),
                  (-L/2.0 + pad,  W/2.0 + pad),
                  (-L/2.0 + pad, -W/2.0 - pad),
                  (-L/2.0 - pad, -W/2.0 - pad)]

            ohmic = Feature(ps)
            self.register_feature(ohmic, 0, 0, 0, 1)
            
            # Right side ohmic
            ps = [(L/2.0 - pad,  W/2.0 + pad),
                  (L/2.0 + pad,  W/2.0 + pad),
                  (L/2.0 + pad, -W/2.0 - pad),
                  (L/2.0 - pad, -W/2.0 - pad)]

            ohmic = Feature(ps)
            self.register_feature(ohmic, 0, 0, 0, 1)

