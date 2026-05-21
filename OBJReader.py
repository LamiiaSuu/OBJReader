import math

def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def norm(v):
    l = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    return (0.0, 0.0, 0.0) if l == 0 else (v[0]/l, v[1]/l, v[2]/l)

def add(a, b): return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def compute_normals(vertices, faces):
    nrm = [(0.0, 0.0, 0.0) for _ in vertices]

    for face in faces:
        idx = [v[0] - 1 for v in face]
        v0 = vertices[idx[0]]

        for i in range(1, len(idx) - 1):
            v1 = vertices[idx[i]]
            v2 = vertices[idx[i + 1]]
            fn = norm(cross(sub(v1, v0), sub(v2, v0)))

            nrm[idx[0]] = add(nrm[idx[0]], fn)
            nrm[idx[i]] = add(nrm[idx[i]], fn)
            nrm[idx[i + 1]] = add(nrm[idx[i + 1]], fn)

    return [norm(n) for n in nrm]

def read_obj(file_path):
    vertices = []
    vertexCount = 0
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
                vertices.append(tuple(map(float, parts[1:4])))
                vertexCount += 1 

            
            elif prefix == 'f':
                face = []
                face_vertices = []
                if len(parts)-1 > maxVert:
                    maxVert = len(parts)-1 
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
        "textureCoordinates": textureCoordinates,
        "maxVert": maxVert,
        "vertexCount": vertexCount
    }


def write_ply(path, vertices, normals, faces):
    tris = []
    for face in faces:
        idx = [v[0] - 1 for v in face]
        for i in range(1, len(idx) - 1):
            tris.append((idx[0], idx[i], idx[i + 1]))

    with open(path, "w", encoding="utf-8") as f:
        f.write("ply\nformat ascii 1.0\n")
        f.write(f"element vertex {len(vertices)}\n")
        f.write("property float x\nproperty float y\nproperty float z\n")
        f.write("property float nx\nproperty float ny\nproperty float nz\n")
        f.write(f"element face {len(tris)}\n")
        f.write("property list uchar int vertex_indices\n")
        f.write("end_header\n")

        for v, n in zip(vertices, normals):
            f.write(f"{v[0]} {v[1]} {v[2]} {n[0]} {n[1]} {n[2]}\n")

        for a, b, c in tris:
            f.write(f"3 {a} {b} {c}\n")

if __name__ == "__main__":
    obj_data = read_obj("cow.obj")

    print(f"has Texture Coordiantes:    {obj_data['textureCoordinates']}")
    print(f"has Normals:    {obj_data['normals']}")
    print(f"Maximum Vertices / Polygon: {obj_data['maxVert']}")
    print(f"Vertices:  {obj_data['vertexCount']}")
    print(f"Edges:  {len(obj_data['edges'])}")
    print(f"Faces:     {len(obj_data['faces'])}")
    normals = compute_normals(obj_data["vertices"], obj_data["faces"])
    write_ply("cow.ply", obj_data["vertices"], normals, obj_data["faces"])