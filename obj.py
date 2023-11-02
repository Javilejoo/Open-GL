from model import Model
class Obj(object):
    def __init__(self, fileName, textureName):
        # Asumiendo que el archivo es un formato .obj
        with open(fileName) as file:
            # Se crean los contenedores de los datos del modelo.
            self.vertices = []
            self.texCoords = []
            self.normals = []
            self.faces = []
            # Por cada l�nea en el archivo
            for line in file:
                # Dependiendo del prefijo, parseamos y guardamos la informaci�n
                # en el contenedor correcto
                if line.startswith("v "):
                    self.vertices.append(list(map(float, line.split()[1:])))
                elif line.startswith("vt "):
                    self.texCoords.append(list(map(float, line.split()[1:])))
                elif line.startswith("vn "):
                    self.normals.append(list(map(float, line.split()[1:])))
                elif line.startswith("f "):
                    face = []
                    for vertex in line.split()[1:]:
                        indices = list(map(int, vertex.split("/")))
                        face.append(indices)
                    self.faces.append(face)

        self.data = self.dataobj()
        self.model = Model(self.data)
        self.model.loadTexture(textureName)

    def dataobj(self):
        data = []
        for face in self.faces:
            for vertexInfo in face:
                vertexId, textureID, normalId = vertexInfo
                vertex = self.vertices[vertexId - 1]
                normals = self.normals[normalId - 1]
                uv = self.texCoords[textureID - 1]
                data.extend(vertex + uv + normals)
        return data