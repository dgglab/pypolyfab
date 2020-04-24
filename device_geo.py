import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
import shapely.affinity as affine

class Device:
    def __init__(self):
        self.features = []

    def register_feature(self, feature, delx, dely, theta):
        """
        Register a feature to the device. Allows one to shift the position of
        the feature in the coordinates of the device
        """
        feature.rotate_and_offset(delx,dely,theta)
        self.features.append(feature)


    def register_feature_group(self, feature_group, delx, dely, theta):
        for feature in feature_group.features:
            self.register_feature(feature, delx, dely, theta)


    def rotate_and_offset_device(self, delx, dely, theta):
        for feature in self.features:
            feature.rotate_and_offset(delx, dely, theta)


    #def join_features(self):

    #def plot():

    #def DXF_output():

    #def grow():



class Feature:
    def __init__(self, ps, layer):
        """
        Generates a shapely polygon for a given feature

        ps: list of tuples of points for polygon
        layer: layer the polygon will live in in cad
        """
        self.update_shape(ps)
        self.set_layer(layer)


    def set_layer(self, layer):
        self.layer = layer


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
        self.poly =  orient(self.poly,-1)


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
