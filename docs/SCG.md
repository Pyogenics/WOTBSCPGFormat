# SCG

This file contains geometric data of the model.

```cpp
struct SCG {
  SCGHeader header;
  SCGBody body;
}
```

## Header

There are two node counts with the same value. Our implementation uses the first node count however the reason behind why there's two is unknown.

- Magic: should always be `"SCPG"`.
- Version: should always be `1`

```cpp
struct SCGHeader {
  char magic[4];
  uint32 version;
  uint32 nodeCount;
  uint32 nodeCount2;
}
```

## Body

The rest of the file is just keyed archives.

```cpp
struct SCGBody {
  KA polygonGroups[header.nodeCount];
}
```

## Polygon group

- Name: always `"PolygonGroup"`
- Id: an 8 byte buffer and can be interpreted as a `uint64`.
- Cube texture coordinates count: how many coordinates for a cube texture is in this group.
- Index count: the number of entries in `indices`.
- Index format: the format of `indices`; 0 means `indices` is an array of `uint16` and 1 means an array of `uint32`.
- Indices: the indices of the mesh as an array of integers.
- Packing: it is unknown what this does; doesn't seem to affect the mesh.
- Primitive count: the number of primitives in `vertices`.
- Render hardware interface primitive type: what type of vertices is in `vertices`.
- Texture coordinates count: the number of texture coordinates in `vertices`.
- Vertex count: the number of vertices.
- Vertex format: a `uint32` that represents the format of the attributes of vertices in `vertices`.
  - To check if a vertex attribute is present, mask a bit shifted one with the format integer and see if it isn't 0.
    - Example: `vertexFormat & 1 << VertexAttribute.TANGENT != 0` will be true if the tangent property is present for all vertices.
  - To get the full format of a single vertex, map through all members of `VertexAttribute` (incrementing order) and generate a list of all present attributes.
  - The aquired format is repeated `vertexCount` number of times.
    - Example: if the resulting format is `[VertexAttribute.VERTEX, VertexAttribute.TEXCOORD0, VertexAttribute.NORMAL]`, the entirety of `vertices` will be `Vector3 normal`, `Vector2 texcoord0`, and `Vector3 normal` over and over again.
    - The vector sizes of each vertex attribute type is documented below as `vertexAttributeVectorSizes`
  - Note that all vertices have the `VertexAttribute.VERTEX` attribute.
- Assembling the indices and vertices appropriately will result in a 3d mesh.

```ts
interface PolygonGroup {
  "##name": "PolygonGroup";
  "#id": Buffer;
  cubeTextureCoordCount: number;
  indexCount: number;
  indexFormat: 0 | 1;
  indices: Buffer;
  packing: 0 | 1;
  primitiveCount: number;
  rhi_primitiveType: RHIPrimitiveType;
  textureCoordCount: number;
  vertexCount: number;
  vertexFormat: number;
  vertices: Buffer;
}
```

### Primitives

```cpp
enum RHIPrimitiveType {
  TRIANGLELIST = 1,
  TRIANGLESTRIP = 2,
  LINELIST = 10,
}
```

This documentation will only discuss information native to SCPG.

- Vertex: always present in all vertices.
- Texture & cube texture coordinates: use the first available entry when trying to access highest lod textures.
- Hard joint index: serves as a discriminator for vertices; can be used to split up the mesh; is used to split up the armor plates on the armor models.
- Pivot deprecated: you should never encounter this.

```cpp
enum VertexAttribute {
  VERTEX = 0,
  NORMAL = 1,
  COLOR = 2,
  TEXCOORD0 = 3,
  TEXCOORD1 = 4,
  TEXCOORD2 = 5,
  TEXCOORD3 = 6,
  TANGENT = 7,
  BINORMAL = 8,
  HARD_JOINTINDEX = 9,
  PIVOT4 = 10,
  PIVOT_DEPRECATED = 11,
  FLEXIBILITY = 12,
  ANGLE_SIN_COS = 13,
  JOINTINDEX = 14,
  JOINTWEIGHT = 15,
  CUBETEXCOORD0 = 16,
  CUBETEXCOORD1 = 17,
  CUBETEXCOORD2 = 18,
  CUBETEXCOORD3 = 19,
}
```

```ts
const vertexAttributeVectorSizes = {
  [VertexAttribute.VERTEX]: 3,
  [VertexAttribute.NORMAL]: 3,
  [VertexAttribute.COLOR]: 1,
  [VertexAttribute.TEXCOORD0]: 2,
  [VertexAttribute.TEXCOORD1]: 2,
  [VertexAttribute.TEXCOORD2]: 2,
  [VertexAttribute.TEXCOORD3]: 2,
  [VertexAttribute.TANGENT]: 3,
  [VertexAttribute.BINORMAL]: 3,
  [VertexAttribute.HARD_JOINTINDEX]: 1,
  [VertexAttribute.CUBETEXCOORD0]: 3,
  [VertexAttribute.CUBETEXCOORD1]: 3,
  [VertexAttribute.CUBETEXCOORD2]: 3,
  [VertexAttribute.CUBETEXCOORD3]: 3,
  [VertexAttribute.PIVOT4]: 4,
  [VertexAttribute.PIVOT_DEPRECATED]: 3,
  [VertexAttribute.FLEXIBILITY]: 1,
  [VertexAttribute.ANGLE_SIN_COS]: 2,
  [VertexAttribute.JOINTINDEX]: 4,
  [VertexAttribute.JOINTWEIGHT]: 4,
};
```
