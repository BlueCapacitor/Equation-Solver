'''
Created on Sep 10, 2020

@author: gosha
'''

from math import pi
from Graphing3D.geometry import Point, Triangle, Surface, sphericalCoords


def sphereUV(center, r, s):
    if(type(s) in [float, int]):
        s = (s, s)

    su, sv = s

    triangles = []

    for u in range(su):
        thetaStart = (u) / su * 2 * pi
        thetaStop = (u + 1) / su * 2 * pi
        for v in range(sv):
            phiStart = (v) / sv * pi
            phiStop = (v + 1) / sv * pi

            triangles.append(Triangle(
                Point([r, thetaStart, phiStart], sphericalCoords),
                Point([r, thetaStop, phiStart], sphericalCoords),
                Point([r, thetaStop, phiStop], sphericalCoords)))
            triangles.append(Triangle(
                Point([r, thetaStart, phiStart], sphericalCoords),
                Point([r, thetaStart, phiStop], sphericalCoords),
                Point([r, thetaStop, phiStop], sphericalCoords)))

    surface = Surface(triangles)
    surface += center
    return(surface)
