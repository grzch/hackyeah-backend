import string

import math

PRISM = 0
PYRAMID = 1

MORE_VERTICES_NUMBERS = {
    PRISM: 4,
    PYRAMID: 1
}


class Vertex:
    x = 0
    y = 0
    z = 0
    angle = 0

    def __init__(self, x=0, y=0, z=0, a=0):
        self.x = x
        self.y = y
        self.z = z
        self.angle = a

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Square:
    def __init__(self, ab):
        self.ab = float(ab)
        self.bc = float(ab)
        self.cd = float(ab)
        self.da = float(ab)
        self.h = float(ab)


class Rectangle:
    def __init__(self, ab, bc):
        self.ab = float(ab)
        self.bc = float(bc)
        self.cd = float(ab)
        self.da = float(bc)
        self.h = float(bc)


class Trapeze:
    def __init__(self, ab, bc, cd, da, h):
        self.ab = float(ab)
        self.bc = float(bc)
        self.cd = float(cd)
        self.da = float(da)
        self.h = float(h)


class Plane:
    def __init__(self, block_type, definitions):
        self.definitions = definitions
        self.height = 0
        self.angle = 90
        self.vertices = {}
        self.connections = set()
        self.parsed_connections = []
        self.base = None
        self.block_type = block_type
        self.base_vertices_number = 0
        self.base_vertices = []

        self.find_data()
        self.prepare_vertices()

        self.calculate_coordinates()

    def find_data(self):
        sections = list(filter(lambda x: x['type'] == 'S', self.definitions))
        angles = list(filter(lambda x: x['type'] == 'A', self.definitions))
        self.angle = float(list(filter(lambda x: x['value'] != '?', self.definitions))[0]['value'])
        self.height = float(int(list(filter(lambda x: x['type'] == 'h', self.definitions))[0]['value']))

        if len(sections) == 1:
            ab = list(filter(lambda x: x['label'] == 'AB', sections))[0]['value']
            self.base = Square(ab)
        elif len(sections) == 2 and len(angles) == 1:
            ab = list(filter(lambda x: x['label'] == 'AB', sections))[0]['value']
            bc = list(filter(lambda x: x['label'] == 'BC', sections))[0]['value']
            self.base = Rectangle(ab, bc)
        else:
            ab = list(filter(lambda x: x['label'] == 'AB' or x['label'] == 'BA', sections))[0]['value']
            bc = list(filter(lambda x: x['label'] == 'BC' or x['label'] == 'CB', sections))[0]['value']
            cd = list(filter(lambda x: x['label'] == 'CD' or x['label'] == 'DC', sections))[0]['value']
            da = list(filter(lambda x: x['label'] == 'DA' or x['label'] == 'AD', sections))[0]['value']
            h = list(filter(lambda x: x['type'] == 'H', self.definitions))[0]['value']
            self.base = Trapeze(ab, bc, cd, da, h)

    def prepare_vertices(self):
        vertices_labels = ['A', 'B', 'C', 'D']
        vertices = set()

        for v in vertices_labels:
            vertices.add(v)

        self.base_vertices_number = len(vertices)
        self.base_vertices = list(vertices)

        for i in range(MORE_VERTICES_NUMBERS[self.block_type]):
            vertices.add(string.ascii_uppercase[self.base_vertices_number + i])

        for v in sorted(vertices):
            self.vertices.update({v: Vertex()})

        self.set_connections()

    def set_connections(self):
        for definition in self.definitions:
            vertices = sorted(definition['vertices'])
            if len(definition['vertices']) == 2:
                self.connections.add((vertices[0], vertices[1], definition['value']))

        if self.block_type == PRISM:
            for definition in self.definitions:
                if len(definition['vertices']) == 2:
                    vertices = sorted(definition['vertices'])
                    self.connections.add((
                        self.get_top_vertex_equivalent(vertices[0]),
                        self.get_top_vertex_equivalent(vertices[1]),
                        definition['value']
                    ))
            for vertex in self.base_vertices:
                self.connections.add((
                    vertex,
                    self.get_top_vertex_equivalent(vertex),
                    self.height
                ))
        elif self.block_type == PYRAMID:
            top_vertex = string.ascii_uppercase[self.base_vertices_number]
            for vertex in self.base_vertices:
                self.connections.add((
                    vertex,
                    top_vertex
                ))

        for connection in self.connections:
            self.parsed_connections.append({
                'from': connection[0],
                'to': connection[1]
            })

    def get_top_vertex_equivalent(self, v):
        return string.ascii_uppercase[string.ascii_uppercase.index(v) + MORE_VERTICES_NUMBERS[self.block_type]]

    def calculate_coordinates(self):
        h = self.base.h
        ab = self.base.ab
        self.vertices.get('B').x = ab

        vertex_b = self.vertices.get('B')
        coords_c = (vertex_b.x + self.base.bc, vertex_b.y, vertex_b.z)
        beta = math.asin(h/self.base.bc)
        re_beta = math.radians(180) - beta
        cx, cy = self.rotate((vertex_b.x, vertex_b.y), (coords_c[0], coords_c[1]), re_beta)
        self.vertices.get('C').set(cx, cy, 0)
        dx = cx - self.base.cd
        dy = cy
        self.vertices.get('D').set(dx, dy, 0)

        for v in ['A', 'B', 'C', 'D']:
            v_prim = self.get_top_vertex_equivalent(v)
            vertex = self.vertices.get(v)
            self.vertices.get(v_prim).set(vertex.x, vertex.y, vertex.z + h)

    @staticmethod
    def rotate(origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return round(qx, 2), round(qy, 2)
