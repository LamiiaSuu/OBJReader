import math

def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def norm(v):
    l = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    return (0.0, 0.0, 0.0) if l == 0 else (v[0]/l, v[1]/l, v[2]/l)

def add(a, b): return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

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
                face_vertices = []

                for vertex in parts[1:]:
                    values = vertex.split("/")
                    v_idx = int(values[0]) if values[0] else None
                    vt_idx = int(values[1]) if len(values) > 1 and values[1] else None
                    vn_idx = int(values[2]) if len(values) > 2 and values[2] else None
                    face.append((v_idx, vt_idx, vn_idx))
                    face_vertices.append(v_idx)
                faces.append(face)

                n = len(face_vertices)

                for i in range(n):
                    a = face_vertices[i]
                    b = face_vertices[(i + 1) % n]
                    edges.add(tuple(sorted((a, b))))


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
    obj_data = read_obj("cow.obj")

    print(f"has Texture Coordiantes:    {obj_data['textureCoordiantes']}")
    print(f"has Normals:    {obj_data['normals']}")
    print(f"Maximum Vertices / Polygon: {obj_data['maxVert']}")
    print(f"Vertices:  {obj_data['vertices']}")
    print(f"Edges:  {len(obj_data['edges'])}")
    print(f"Faces:     {len(obj_data['faces'])}")