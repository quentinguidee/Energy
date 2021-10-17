def eval_projected_area(face, obj):
    """
    Calculate the z projected surface of a face
    """
    area = 0.0
    transform_matrix = obj.matrix_world

    vertices_count = len(face.vertices)
    vertices = []

    for i in range(vertices_count):
        vertex_id = face.vertices[i]
        vertex = obj.data.vertices[vertex_id]
        transformed_vertex = transform_matrix @ vertex.co
        transformed_vertex[2] = 0
        vertices.append(transformed_vertex)

    if vertices_count == 4:
        vector0 = vertices[1] - vertices[0]
        vector1 = vertices[3] - vertices[0]

        n = vector0.cross(vector1)

        area = n.length / 2.0

        vector0 = vertices[3] - vertices[2]
        vector1 = vertices[1] - vertices[2]

        n = vector0.cross(vector1)

        area += n.length / 2.0

    elif vertices_count == 3:
        vector0 = vertices[2] - vertices[1]
        vector1 = vertices[0] - vertices[1]

        n = vector0.cross(vector1)

        area = n.length / 2.0

    return area
