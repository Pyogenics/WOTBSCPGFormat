# .SCG

SCene Geometry, the largest out of the two files, contains model data. File made up of a header followed by a series of keyed archives.<br><br>
Example file snippet (hexdump with ascii view):

```
00000010  4b 41 01 00 0d 00 00 00  04 06 00 00 00 23 23 6e  |KA...........##n|
00000020  61 6d 65 04 0c 00 00 00  50 6f 6c 79 67 6f 6e 47  |ame.....PolygonG|
00000030  72 6f 75 70 04 03 00 00  00 23 69 64 06 08 00 00  |roup.....#id....|
00000040  00 ed 00 00 00 00 00 00  00 04 15 00 00 00 63 75  |..............cu|
00000050  62 65 54 65 78 74 75 72  65 43 6f 6f 72 64 43 6f  |beTextureCoordCo|
00000060  75 6e 74 02 00 00 00 00  04 0a 00 00 00 69 6e 64  |unt..........ind|
00000070  65 78 43 6f 75 6e 74 02  58 05 00 00 04 0b 00 00  |exCount.X.......|
00000080  00 69 6e 64 65 78 46 6f  72 6d 61 74 02 00 00 00  |.indexFormat....|
00000090  00 04 07 00 00 00 69 6e  64 69 63 65 73 06 b0 0a  |......indices...|
```

## Header

The file starts with "SCPG", aka the magic `53 43 50 47` and contains a small header of 12 bytes made up of: version, node count and a second node count (seems to match the first, could count a certain node type?).

```c
struct SCGHeader
{
    uint32_t version;       // Should be 1
    uint32_t nodeCount;
    uint32_t nodeCount2;
}
```

Example header: `53 43 50 47 01 00 00 00  53 00 00 00 53 00 00 00` - SCPG version 1 with 53 nodes

## Keys/Values

### \#\#name

Name of the KA, acts like a type; know names:

- PolygonGroup

## Polygon group

This type of KA stores polygons, literally a group of polygons + additional info.

### \#id

Byte array of unknown purpose, some kind of unique engine internal field?.

### cubeTextureCoordCount

Number of cube texture coords in this polygon group.

### indexCount

Number of indices stored in the index array

### indexFormat

Size of each index in the index array (0 = uint16 1 = uint32).

```c
int32 INDEX_FORMAT_SIZE[2] = {
    2,
    4
};
```

### indices

Index array.

### packing

How the vertex array is packed.

```c
enum
{
    PACKING_NONE = 0,
    PACKING_DEFAULT = 1
};
```

### primitiveCount

Number of primitives contained in this polygon group.

### rhi_primitiveType

What type of primitive this polygon group stores.

```c
enum PrimitiveType
{
    PRIMITIVE_TRIANGLELIST = 1,
    PRIMITIVE_TRIANGLESTRIP = 2,
    PRIMITIVE_LINELIST = 10
};
```

### textureCoordCount

Number of texture coords stored in this polygon group.

### vertexCount

Number of vertices stored in the vertex array.

### vertexFormat

Format of the vertex array, it contains multiple different data types.

### vertices

The vertex array, stores all the vertices of the polygon group.
