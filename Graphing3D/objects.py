'''
Created on Jun 5, 2020

@author: Gosha
'''

from Graphing3D.screen3D import Side


class Color():

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def rgb(self):
        return(self.r, self.g, self.b)


class DPoint(object):

    def __init__(self, point, color = (0, 0, 0), radius = 1):
        self.point = point
        self.color = color
        self.radius = radius

    def draw(self, screen, camera, scale):
        t = screen.t

        cent = camera.project(self.point)
        radius = camera.aproxSphereSize(self.point, self.radius)
        screenDepth = camera.depth(self.point)

        t.up()
        position = [cent[0] * scale, cent[1] * scale]
        if(screenDepth >= 0 and screen.checkBounds(position, (-5, -5))):
            t.goto(*position)
            t.dot(radius * 2 * scale * 0 + 5, self.color)


class DCamera(object):

    def __init__(self, camera, background = (1, 1, 1), objects = []):
        self.camera = camera
        self.background = background
        self.surfaces = objects

    def show(self, Dobject):
        if(Dobject not in self.surfaces):
            self.surfaces.append(Dobject)

    def hide(self, Dobject):
        if(Dobject in self.surfaces):
            self.surfaces.remove(Dobject)

    def clear(self):
        self.surfaces = []

    def extractTriangles(self):
        triangles = []
        for surface in self.surfaces:
            triangles += surface.triangles


class DSurface(object):

    def __init__(self, surface, fill = (0, 0, 0), border = None):
        self.surface = surface
        self.fill = fill
        self.border = border

    def extractDTriangles(self):
        return([DTriangle(triangle, fill = self.fill, border = self.border) for triangle in self.surface.triangles])


class DTriangle(object):

    def __init__(self, triangle, fill = (0, 0, 0), border = None):
        self.triangle = triangle
        self.fill = fill
        self.border = border

    def down(self, t):
        if(self.border != None):
            t.pencolor(self.border)
            t.width(2)
            t.down()
        elif(self.fill != None):
            t.pencolor(self.fill)
            t.width(2)
            t.down()

        if(self.fill != None):
            t.fillcolor(self.fill)
            t.begin_fill()

    def draw(self, screen, *_):
        t = screen.t
        points = self.triangle.points

        target = {}
        p = {}
        s = {}

        for a in range(3):
            for b in range(3):
                if(a != b):
                    target[(a, b)] = screen.target(points[a], points[b])

                    if(target[(a, b)] != None):
                        p[(a, b)], s[(a, b)] = target[(a, b)]

        if(all(map(lambda x: x == None, target.values()))):
            return

        if(all(map(lambda x: x != None, target.values()))):
            t.up()
            t.goto(*p[0, 1])
            self.down(t)

            for a in range(3):
                b = (a + 1) % 3
                c = (a + 2) % 3

                t.goto(*p[(b, a)])
                if(s[(b, a)] != None and s[(b, c)] != None):
                    if(s[(b, a)].isAdjacent(s[(b, c)])):
                        t.goto(*s[(b, a)].intersection(s[(b, c)]))

                    if(s[(b, a)].isOpposite(s[(b, c)])):
                        o = findOpposite2(screen, p, s, a, b, c)

                        if(o == None):
                            return

                        t.goto(*s[(b, a)].intersection(o))
                        t.goto(*s[(b, c)].intersection(o))

                    t.goto(*p[(b, c)])
                else:
                    t.goto(*p[(b, c)])

            t.up()
            t.end_fill()
            return

        for a in range(2):
            for b in range(a + 1, 3):
                if(target[(a, b)] == None):
                    break
            else:
                continue
            break

        c = [[None, 2, 1], [None, None, 0]][a][b]

        if(None in (target[(a, c)], target[(b, c)], target[(c, a)], target[(c, b)])):
            return

        if(s[(a, c)] == s[(b, c)]):
            t.up()
            t.goto(*p[a, c])
            self.down(t)
            t.goto(*p[c, a])
            t.goto(*p[c, b])
            t.goto(*p[b, c])
            t.goto(*p[a, c])
            t.up()
            t.end_fill()
        if(s[(a, c)].isAdjacent(s[(b, c)])):
            t.up()
            t.goto(*p[a, c])
            self.down(t)
            t.goto(*p[c, a])
            t.goto(*p[c, b])
            t.goto(*p[b, c])
            t.goto(*s[b, c].intersection(s[a, c]))
            t.goto(*p[a, c])
            t.up()
            t.end_fill()
        if(s[(a, c)].isOpposite(s[(b, c)])):
            o = findOpposite(screen, p, s, a, b, c)

            if(o == None):
                return

            t.up()
            t.goto(*p[a, c])
            self.down(t)
            t.goto(*p[c, a])
            t.goto(*p[c, b])
            t.goto(*p[b, c])
            t.goto(*s[b, c].intersection(o))
            t.goto(*s[a, c].intersection(o))
            t.goto(*p[a, c])
            t.up()
            t.end_fill()


def findOpposite(screen, p, s, a, b, c):  # opposite side from c
    if(s[(c, a)] != None and s[(c, b)] != None):
        o = s[(c, a)].opposite()
    else:
        C = p[(c, a)]

        if(p[(a, c)][0] == p[(b, c)][0]):
            if(p[(a, c)][0] > C[0]):
                o = Side(screen, 'R')
            elif(p[(a, c)][0] < C[0]):
                o = Side(screen, 'L')
            else:
                return
        else:
            dy = p[(a, c)][1] - p[(b, c)][1]
            dx = p[(a, c)][0] - p[(b, c)][0]
            m = dy / dx
            L = lambda x: m * (x - p[(a, c)][0]) + p[(a, c)][1]
            LI = lambda y: (1 / m) * (y - p[(a, c)][1]) + p[(a, c)][0]

            if(s[(a, c)].side in ['R', 'L']):
                if(C[1] > L(C[0])):
                    o = Side(screen, 'B')
                elif(C[1] < L(C[0])):
                    o = Side(screen, 'T')
                else:
                    return
            else:
                if(C[0] > LI(C[1])):
                    o = Side(screen, 'L')
                elif(C[0] < LI(C[1])):
                    o = Side(screen, 'R')
                else:
                    return
    return(o)


def findOpposite2(screen, p, s, a, b, c):  # opposite side from b
    if(s[(a, b)] != None and s[(c, b)] != None):
        return(s[(a, b)].opposite())
    else:
        A = p[(a, b)]
        C = p[(c, b)]
        BA = p[(b, a)]
        BC = p[(b, c)]

        if(s[(b, a)].side in ['R', 'L']):
            SYAC = A[1] + C[1]
            SYB = BA[1] + BC[1]

            if(SYAC > SYB):
                return(Side(screen, 'B'))
            if(SYAC < SYB):
                return(Side(screen, 'T'))
            if(SYAC == SYB):
                return

        if(s[(b, a)].side in ['T', 'B"']):
            SXAC = A[0] + C[0]
            SXB = BA[0] + BC[0]

            if(SXAC > SXB):
                return(Side(screen, 'L'))
            if(SXAC < SXB):
                return(Side(screen, 'R'))
            if(SXAC == SXB):
                return
