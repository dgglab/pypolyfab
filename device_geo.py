import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
import shapely.affinity as affine
import ezdxf


class Device:
    '''
    Devices consist of a collection of features which are healed together
    '''

    def __init__(self):
        self.features = {}

    def register_feature(self, feature, delx, dely, theta, layer, origin='center'):
        '''
        Register a feature to the device to the given layer
        Requires translation and rotation arguments to place the Feature in the
        Device coordinate system
        '''
        new_feature = feature.copy()
        new_feature.rotate_and_translate(delx, dely, theta, origin)

        if layer in self.features:
            self.features[layer].append(new_feature)
        else:
            self.features[layer] = [new_feature]

    def heal(self):
        '''
        heals all the polygons together in a given device layer
        '''
        for layer in self.features.keys():
            healed = self.features[layer][0].copy()
            for i, feature in enumerate(self.features[layer]):
                if i != 0:
                    healed.poly = healed.poly.union(feature.poly)

            self.features[layer] = [healed]

    def scale(self, layer, xfact, yfact, origin='center'):
        '''
        Scales each feature in the given layer by xfact and yfact
        Scale can take either center or centroid
        '''
        self.features[layer].scale(xfact, yfact, origin)

    def gen_fig(self):
        '''
        Return a figure of the feature colored by layer
        '''
        fig = plt.figure()
        for layer in self.features.keys():
            for feature in self.features[layer]:
                if type(feature.poly) == Polygon:
                    x, y = feature.poly.exterior.coords.xy
                    plt.plot(x, y, color='C'+str(layer))
                else:
                    for poly in feature.poly:
                        x, y = poly.exterior.coords.xy
                        plt.plot(x, y, color='C'+str(layer))

        return fig

    def write_dxf(self, fname='output.dxf'):
        '''
        Return a dxf file. Writes layers to layers
        '''
        doc = ezdxf.new(dxfversion='R2010', setup=True)
        msp = doc.modelspace()

        for layer in self.features.keys():
            if layer != 0:
                doc.layers.new(name=str(layer), dxfattribs={'color': layer})

            for feature in self.features[layer]:
                if type(feature.poly) == Polygon:
                    msp.add_lwpolyline(list(feature.poly.exterior.coords),
                                       dxfattribs={'layer': str(layer)})
                else:
                    for poly in feature.poly:
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

    def rotate_and_translate(self, delx, dely, theta, origin='center'):
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

    def union(self, ps):
        '''
        Union a new polygon with the feature to form a new combined feature
        Returns an error if the polygons are disjoint
        '''
        new_poly = Polygon(ps)
        new_poly = self.poly.union(new_poly)
        if type(new_poly) != Polygon:
            raise ValueError('Polygons are disjoint')
        else:
            self.poly = new_poly

        self.poly2cw()

    def gen_fig(self):
        '''
        Return a figure of the feature
        '''
        x, y = self.poly.exterior.coords.xy
        fig = plt.figure()
        plt.plot(x, y)
        return fig

    def copy(self):
        return Feature(self.poly.exterior.coords)
