import string

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


class Plane:
    def __init__(self, block_type, definitions):
        self.height = 0
        self.max_width = 0
        self.definitions = definitions
        self.view_width = 0.5
        self.view_height = 2 * self.view_width
        self.vertices = {}
        self.connections = set()
        self.parsed_connections = []
        self.block_type = block_type
        self.base_vertices_number = 0
        self.base_vertices = []

        self.prepare_vertices()

        print(self.vertices)
        print(self.connections)

    def prepare_vertices(self):
        vertices = set()
        for definition in self.definitions:
            if len(definition['vertices']) == 2:
                for v in definition['vertices']:
                    vertices.add(v)
            elif len(definition['vertices']) == 1:  # height
                self.height = int(definition['value'])

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

    def get_length(self, v1, v2):
        vertices = sorted([v1, v2])
        length = list(filter(lambda x: x[0] == vertices[0] and x[1] == vertices[1], self.connections))
        return length[0]

    def get_top_vertex_equivalent(self, v):
        return string.ascii_uppercase[string.ascii_uppercase.index(v) + MORE_VERTICES_NUMBERS[self.block_type]]
