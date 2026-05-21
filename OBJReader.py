def read_obj(file_path):
    vertices = 0
    maxVert = 0
    edges = set()
    normals = False
    faces = []
    textureCoordinates = False

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()
            prefix = parts[0]

            if prefix == 'v':
                vertices += 1
                if len(parts)-1 > maxVert:
                    maxVert = len(parts)-1 
            
            elif prefix == 'f':
                face = []
                for vertex in parts[1:]:
                    values = vertex.split("/")
                    v_idx = int(values[0]) if values[0] else None
                    vt_idx = int(values[1]) if len(values) > 1 and values[1] else None
                    vn_idx = int(values[2]) if len(values) > 2 and values[2] else None
                    face.append((v_idx, vt_idx, vn_idx))
                faces.append(face)


            elif prefix == "vt":
                textureCoordinates = True

            elif prefix == "vn":
                normals = True


    return {
        "vertices": vertices,
        "edges": edges,
        "normals": normals,
        "faces": faces,
        "textureCoordiantes": textureCoordinates,
        "maxVert": maxVert
    }


if __name__ == "__main__":
    obj_data = read_obj("bunny.obj")

    print(f"has Texture Coordiantes:    {obj_data['textureCoordiantes']}")
    print(f"has Normals:    {obj_data['normals']}")
    print(f"Maximum Vertices / Polygon: {obj_data['maxVert']}")
    print(f"Vertices:  {obj_data['vertices']}")
    print(f"Edges:  {len(obj_data['edges'])}")
    print(f"Faces:     {len(obj_data['faces'])}")