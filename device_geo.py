import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
import shapely.affinity as affine
import copy
import ezdxf


class Device:
    '''
    Devices consist of a collection of features which are healed together
    '''

    def __init__(self):
        self.features = {}

        self.device = {}

    def register_feature(self, feature, layer):
        '''
        Register a feature to the device to the given layer
        '''
        if layer in self.features:
            self.features[layer].append(feature)
        else:
            self.features[layer] = [feature]

    def heal(self):
        '''
        heals all the polygons together in a given device layer
        '''
        for layer in self.features.keys():
            self.device[layer] = copy.copy(self.features[layer][0])
            for feature in self.features[layer]:
                self.device[layer].poly = self.device[layer].poly.union(
                    feature.poly)

    def scale(self, layer, xfact, yfact, origin='center'):
        '''
        Scales each feature in the given layer by xfact and yfact
        Scale can take either center or centroid
        '''
        self.device[layer].scale(xfact, yfact, origin)

    def gen_fig(self):
        '''
        Return a figure of the feature colored by layer
        '''
        fig = plt.figure()
        for layer in self.device.keys():
            if type(self.device[layer].poly) == Polygon:
                x = [x[0]
                     for x in list(self.device[layer].poly.exterior.coords)]
                y = [x[1]
                     for x in list(self.device[layer].poly.exterior.coords)]
                plt.plot(x, y, color='C'+str(layer))
            else:
                for poly in self.device[layer].poly:
                    x = [x[0] for x in list(poly.exterior.coords)]
                    y = [x[1] for x in list(poly.exterior.coords)]
                    plt.plot(x, y, color='C'+str(layer))

        return fig

    def write_dxf(self, fname='output.dxf'):
        '''
        Return a dxf file. Writes layers to layers
        '''
        doc = ezdxf.new(dxfversion='R2010', setup=True)
        msp = doc.modelspace()

        for layer in self.device.keys():
            if layer != 0:
                doc.layers.new(name=str(layer), dxfattribs={'color': layer})

            if type(self.device[layer].poly) == Polygon:
                msp.add_lwpolyline(list(self.device[layer].poly.exterior.coords),
                                   dxfattribs={'layer': str(layer)})
            else:
                for poly in self.device[layer].poly:
                    msp.add_lwpolyline(list(poly.exterior.coords),
                                       dxfattribs={'layer': str(layer)})

        doc.saveas(fname)


class Feature:
    '''
    A feature should be considered a single polygon which can be combined with other
    features to form a device
    '''

    def __init__(self, ps):
        """
        Generates a shapely polygon for a given feature

        ps: list of tuples of points for polygon
        """
        self.update_shape(ps)

    def update_shape(self, ps):
        """
        updates the coordinates of the polygon and sets to be clockwise
        """
        self.poly = Polygon(ps)
        self.poly2cw()

    def poly2cw(self):
        '''
        Forces verticies of polygon to be clockwise
        '''
        self.poly = orient(self.poly, -1)

    def rotate_and_offset(self, delx, dely, theta, origin='center'):
        '''
        Rotate and translate the polygon
        Rotate can take either center or centroid
        '''
        self.poly = affine.rotate(self.poly, theta, origin)
        self.poly = affine.translate(self.poly, delx, dely)

    def scale(self, xfact, yfact, origin='center'):
        '''
        Scale the feature by xfact and yfact
        Scale can take either center or centroid
        '''
        self.poly = affine.scale(self.poly, xfact, yfact, 1, origin)

    def gen_fig(self):
        '''
        Return a figure of the feature
        '''
        x = [x[0] for x in list(self.poly.exterior.coords)]
        y = [x[1] for x in list(self.poly.exterior.coords)]
        fig = plt.figure()
        plt.plot(x, y)
        return fig
