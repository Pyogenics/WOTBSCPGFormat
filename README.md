# World Of Tanks: Blitz SCPG model format
Reverse engineered information about the model format used by WOTB.

## Preface
This resource aims to shed light on the model format, "SCPG", used by WOTB and eventually provide tools to modify and create said models.

Models in WOTB are located in `/packs/3d/` and each model comes in a pair of files with extensions `.scg` and `.sc2`, for example: `packs/3d/Tanks/German/Maus.scg` `packs/3d/Tanks/German/Maus.sc2`. Game files are compressed using the `dvpl` format, you can use [this](https://github.com/Tankerch/DVPL_Converter) tool to decompress them.

Current work is based on SC2 version 41.

## Blender plugin
Read about it [here](blender/README.md)

## Sources
An old version of the DAVA engine is available [here](https://github.com/smile4u/dava.engine).
- [KeyedArchive](https://github.com/smile4u/dava.engine/blob/development/Sources/Internal/FileSystem/KeyedArchive.cpp)
- [KeyedArchive data R/W](https://github.com/smile4u/dava.engine/blob/development/Sources/Internal/FileSystem/VariantType.cpp)
- [SceneFileV2](https://github.com/smile4u/dava.engine/blob/development/Sources/Internal/Scene3D/SceneFileV2.cpp)
- [PolygonGroup](https://github.com/smile4u/dava.engine/blob/development/Sources/Internal/Render/3D/PolygonGroup.cpp)

## Keyed Archive
Keyed archives are binary blobs stored inside both `.sc2` and `.scg` files that are used to store key/value pairs. Each keyed archive is identified with the magic "KA" (`4b 41`) and contains a small header, key/value pairs come directly after the header.
### Header
```c
struct KAHeader
{
    uint16_t version;
    uint32_t itemCount;
}
```
### Version 1
Each entry in a version 1 KA is identified by a 1 byte data type followed by the actual data, the data is read based on its' data type.
```c
struct KAEntry_v1
{
    uint8_t dataType;
    uint8_t data[];
}
```
### Version 2
Only seen inside `.sc2` files; data seems to be packed tightly together compared to version 1.

Seems to be an array of strings with the format.
```c
struct KAEntry_v2
{
    uint16_t length;
    char string[];
}
```
Seemingly followed by a binary blob of somekind.
### Version 258
Only seen inside `.sc2` in varying sizes, doesn't seem to contain any strings.

## .SCG
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
### Header
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
### Keys/Values
#### \#\#name
Name of the KA, acts like a type; know names:
- PolygonGroup
### Polygon group
This type of KA stores polygons, literally a group of polygons + additional info.

#### \#id
Byte array of unknown purpose, some kind of unique engine internal field?.
#### cubeTextureCoordCount
Number of cube texture coords in this polygon group.
#### indexCount
Number of indices stored in the index array
#### indexFormat
Size of each index in the index array (0 = uint16 1 = uint32).

```c
int32 INDEX_FORMAT_SIZE[2] = {
    2,
    4
};
```
#### indices
Index array.
#### packing
How the vertex array is packed.

```c
enum
{
    PACKING_NONE = 0,
    PACKING_DEFAULT = 1
};
```
#### primitiveCount
Number of primitives contained in this polygon group.
#### rhi\_primitiveType
What type of primitive this polygon group stores.

```c
enum PrimitiveType
{
    PRIMITIVE_TRIANGLELIST = 1,
    PRIMITIVE_TRIANGLESTRIP = 2,
    PRIMITIVE_LINELIST = 10
};
```
#### textureCoordCount
Number of texture coords stored in this polygon group.
#### vertexCount
Number of vertices stored in the vertex array.
#### vertexFormat
Format of the vertex array, it contains multiple different data types.
#### vertices
The vertex array, stores all the vertices of the polygon group.

## .SC2
SCene file v2, smallest file, contains scene information and references to resources like textures.
### Header
The file starts with "SFV2" (magic: `53 46 56 32`) and contains a small header of 8 bytes made up of version and node count. This is followed by a KA containing "version tags", file descriptor and data node count. The header is followed by keyed archives.
```c
struct SC2Header
{
    uint32_t version;
    uint32_t nodeCount;
}
```
#### Version tags
Contains version information todo with the scene file.
#### Descriptor
Stores file type information.
```c
struct SC2Descriptor
{
    uint32_t size;
    enum {Scene = 0, Model = 1} fileType; 
    uint8_t otherFields[]; // Newer versions of the file could have additional fields we don't handle
}
```

The descriptor is followed by a `uint32_t` which stores the data node count.
