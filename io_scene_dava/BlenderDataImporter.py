from io import BytesIO
from .Utils import unpackStream
import bpy

class PolygonGroup:
    INDEX_TYPE_INT16 = 0
    INDEX_TYPE_INT32 = 1

    VERTEX_TYPE_VERTEX = 1
    VERTEX_TYPE_NORMAL = 1 << 1
    VERTEX_TYPE_COLOR = 1 << 2
    VERTEX_TYPE_TEXCOORD0 = 1 << 3
    VERTEX_TYPE_TEXCOORD1 = 1 << 4
    VERTEX_TYPE_TEXCOORD2 = 1 << 5
    VERTEX_TYPE_TEXCOORD3 = 1 << 6
    VERTEX_TYPE_TANGENT = 1 << 7
    VERTEX_TYPE_BINORMAL = 1 << 8
    VERTEX_TYPE_HARDJOINTINDEX = 1 << 9
    VERTEX_TYPE_PIVOT4 = 1 << 10
    VERTEX_TYPE_FLEXIBILITY = 1 << 12
    VERTEX_TYPE_ANGLESINCOS = 1 << 13
    VERTEX_TYPE_JOINTINDEX = 1 << 14
    VERTEX_TYPE_JOINTWEIGHT = 1 << 15
    VERTEX_TYPE_CUBETEXCOORD0 = 1 << 16
    VERTEX_TYPE_CUBETEXCOORD1 = 1 << 17
    VERTEX_TYPE_CUBETEXCOORD2 = 1 << 18
    VERTEX_TYPE_CUBETEXCOORD3 = 1 << 19

    PRIMITIVE_TYPE_TRIANGLES = 1
    PRIMITIVE_TYPE_TRIANGLESTRIP = 2
    PRIMITIVE_TYPE_LINELIST = 10

    def __init__(self, node):
        self.vertexCount = node["vertexCount"]
        self.indexCount = node["indexCount"]
        self.primitiveType = node["rhi_primitiveType"]
        self.primitiveCount = node["primitiveCount"]

        # Process index data
        self.indices = []

        indexBuffer = BytesIO(node["indices"])
        indexFormat = node["indexFormat"]
        if indexFormat == PolygonGroup.INDEX_TYPE_INT16:
            self.indices = list(
                unpackStream(f"<{self.indexCount}H", indexBuffer)
            )
        elif indexFormat == PolygonGroup.INDEX_TYPE_INT32:
            self.indices = list(
                unpackStream(f"<{self.indexCount}I", indexBuffer)
            )
        else:
            raise RuntimeError(f"Unknown index format: {indexFormat}")

        # Process vertex data
        self.vertices = []
        self.normals = []
        self.colors = []
        self.texcoord0 = []
        self.texcoord1 = []
        self.texcoord2 = []
        self.texcoord3 = []
        self.tangents = []
        self.binormals = []
        self.hardjointindices = []
        self.pivot4 = []
        self.flexibility = []
        self.anglesincos = []
        self.jointindices = []
        self.jointweights = []
        self.cubetexcoord0 = []
        self.cubetexcoord1 = []
        self.cubetexcoord2 = []
        self.cubetexcoord3 = []

        vertexBuffer = BytesIO(node["vertices"])
        for _ in range(self.vertexCount):
            vertexFormat = node["vertexFormat"]

            if vertexFormat & PolygonGroup.VERTEX_TYPE_VERTEX:
                vertex = unpackStream("<3f", vertexBuffer)
                self.vertices += list(vertex)
            if vertexFormat & PolygonGroup.VERTEX_TYPE_NORMAL:
                vertex = unpackStream("<3f", vertexBuffer)
                self.normals += list(vertex)
            if vertexFormat & PolygonGroup.VERTEX_TYPE_COLOR:
                vertex = unpackStream("<f", vertexBuffer)
                self.colors += vertex
            if vertexFormat & PolygonGroup.VERTEX_TYPE_TANGENT:
                vertex = unpackStream("<3f", vertexBuffer)
                self.tangents += list(vertex)
            if vertexFormat & PolygonGroup.VERTEX_TYPE_BINORMAL:
                vertex = unpackStream("<3f", vertexBuffer)
                self.binormals += list(vertex)

            if vertexFormat & PolygonGroup.VERTEX_TYPE_TEXCOORD0:
                vertex = unpackStream("<2f", vertexBuffer)
                self.texcoord0 += list(vertex)
            if vertexFormat & PolygonGroup.VERTEX_TYPE_TEXCOORD1:
                vertex = unpackStream("<2f", vertexBuffer)
                self.texcoord1 += list(vertex)
            if vertexFormat & PolygonGroup.VERTEX_TYPE_TEXCOORD2:
                vertex = unpackStream("<2f", vertexBuffer)
                self.texcoord2 += list(vertex)
            if vertexFormat & PolygonGroup.VERTEX_TYPE_TEXCOORD3:
                vertex = unpackStream("<2f", vertexBuffer)
                self.texcoord3 += list(vertex)

            if vertexFormat & PolygonGroup.VERTEX_TYPE_HARDJOINTINDEX:
                vertex = unpackStream("<f", vertexBuffer)
                self.tangents += vertex
            
            if vertexFormat & PolygonGroup.VERTEX_TYPE_CUBETEXCOORD0:
                vertex = unpackStream("<3f", vertexBuffer)
                self.cubetexcoord0 += list(vertex)
            if vertexFormat & PolygonGroup.VERTEX_TYPE_CUBETEXCOORD1:
                vertex = unpackStream("<3f", vertexBuffer)
                self.cubetexcoord1 += list(vertex)
            if vertexFormat & PolygonGroup.VERTEX_TYPE_CUBETEXCOORD2:
                vertex = unpackStream("<3f", vertexBuffer)
                self.cubetexcoord2 += list(vertex)
            if vertexFormat & PolygonGroup.VERTEX_TYPE_CUBETEXCOORD3:
                vertex = unpackStream("<3f", vertexBuffer)
                self.cubetexcoord3 += list(vertex)
    
            if vertexFormat & PolygonGroup.VERTEX_TYPE_PIVOT4:
                vertex = unpackStream("<4f", vertexBuffer)
                self.pivot4 += list(vertex)
            if vertexFormat & PolygonGroup.VERTEX_TYPE_FLEXIBILITY:
                vertex = unpackStream("<f", vertexBuffer)
                self.flexibility += vertex
            if vertexFormat & PolygonGroup.VERTEX_TYPE_ANGLESINCOS:
                vertex = unpackStream("<2f", vertexBuffer)
                self.anglesincos += list(vertex)
            if vertexFormat & PolygonGroup.VERTEX_TYPE_JOINTINDEX:
                vertex = unpackStream("<4f", vertexBuffer)
                self.jointindices += list(vertex)
            if vertexFormat & PolygonGroup.VERTEX_TYPE_JOINTWEIGHT:
                vertex = unpackStream("<4f", vertexBuffer)
                self.jointweights += list(vertex)
        
        print(f"[PolygonGroup vertexCount={self.vertexCount} indexCount={self.indexCount} primitiveType={self.primitiveType} primitiveCount={self.primitiveCount}]")

class BlenderDataImporter:
    def __init__(self, geometryData):
        self.geometryData = geometryData

        self.polygonGroups = {}

    def importData(self):
        print("Importing data into blender")

        # Process polygon groups
        for geometryNode in self.geometryData.nodes:
            if geometryNode["##name"] != "PolygonGroup":
                raise RuntimeError("Unknown geometry node type: " + geometryNode["##name"])

            polygonGroup = PolygonGroup(geometryNode)
            self.polygonGroups[geometryNode["#id"]] = polygonGroup
        
        # Create meshes
        meshes = {}
        for polygonGroupID in self.polygonGroups:
            polygonGroup = self.polygonGroups[polygonGroupID]

            # Assign data
            meshName = int.from_bytes(polygonGroupID, "little")
            me = bpy.data.meshes.new(f"PolygonGroup_{meshName}")
            me.vertices.add(polygonGroup.vertexCount)
            me.vertices.foreach_set("co", polygonGroup.vertices)
            if polygonGroup.primitiveType == PolygonGroup.PRIMITIVE_TYPE_TRIANGLES:
                me.loops.add(polygonGroup.indexCount)
                me.loops.foreach_set("vertex_index", polygonGroup.indices)
                me.polygons.add(polygonGroup.primitiveCount)
                me.polygons.foreach_set("loop_start", range(0, polygonGroup.indexCount, 3))
            elif polygonGroup.primitiveType == PolygonGroup.PRIMITIVE_TYPE_TRIANGLESTRIP:
                me.loops.add(polygonGroup.indexCount)
                me.loops.foreach_set("vertex_index", polygonGroup.indices)
                me.polygons.add(polygonGroup.primitiveCount)
                me.polygons.foreach_set("loop_start", range(0, polygonGroup.primitiveCount))
            elif polygonGroup.primitiveType == PolygonGroup.PRIMITIVE_TYPE_LINELIST:
                me.edges.add(polygonGroup.primitiveCount)
                me.edges.foreach_set("vertices", polygonGroup.indices)

            # Validate
            me.validate()
            me.update()

            meshes[polygonGroupID] = me
        
        # Create objects
        objects = []
        for meID in meshes:
            me = meshes[meID]
            ob = bpy.data.objects.new(me.name, me)
            objects.append(ob)
        
        return objects