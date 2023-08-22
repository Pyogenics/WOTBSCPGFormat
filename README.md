# World Of Tanks: Blitz SCPG model format
Reverse engineered information about the model format used by WOTB.

## Preface
This resource aims to shed light on the model format, "SCPG", used by WOTB and eventually provide tools to modify and create said models. Wargaming poses tools to work with "SCPG" models however they are proprietary and not much is known about them in the community.

Models in WOTB are located in `/packs/3d/` and each model comes in a pair of files with extensions `.scg` and `.sc2`, for example: `packs/3d/Tanks/German/Maus.scg` `packs/3d/Tanks/German/Maus.sc2`. Game files are compressed using the `dvpl` format, you can use [this](https://github.com/Tankerch/DVPL_Converter) tool to decompress them.

## Blender plugin
Read about it [here](blender/README.md)

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
Each entry in a version 1 KA is identified by a 1 byte data type followed by the actual data, the data is read based on it's data type.
```c
struct KAEntry_v1
{
    uint8_t dataType;
    uint8_t data[];
}
```
### Version 2
Unknown, only seen inside `.sc2` files; data seems to be packed tightly together compared to version 1.

## .SCG
SCene Geometry, the largest out of the two files, contains model data like vertices.
### Header
The file starts with "SCPG", aka the magic `53 43 50 47` and contains a small header of 12 bytes. The 9th and 13th byte contain the number of blobs contained within the file.

Example: `53 43 50 47 01 00 00 00  53 00 00 00 53 00 00 00`
### Blobs
The file is seperated into multiple sections, "blobs", which are of different lengths and seperated by the string "KA" (`4b 41`).

Each blob contains a number of key/value pairs of varying length and seem to always appear in the same order, some values also seem to be the same length between blobs and files. Before the first key/value pair there is a small 11 byte header. Every key/value pair is prepended by three null bytes, `00 00 00`, however splitting the data by `00 00 00` isn't ideal as it can also split value fields if they contain too many zeros.

Key/value pairs in order of appearance:
Key | Value (field + padding)
----|------------------------
`##name`                | 2 + 3 bytes
`PolygonGroup`          | 2 + 3 bytes
`#id`                   | 15 + 3 bytes
`cubeTextureCoordCount` | 7 + 3 bytes
`indexCount`            | 7 + 3 bytes
`indexFormat`           | 17 + 3 bytes
`indices`               | varying length
`packing`               | 7 + 3 bytes
`primitiveCount`        | 7 + 3 bytes
`rhi_primitiveType`     | 7 + 3 bytes
`textureCoordCount`     | 7 + 3 bytes
`vertexCount`           | 7 + 3 bytes
`vertexFormat`          | 7 + 3 bytes
`vertices`              | varying length, stretches to the boundary of the next blob

Example snippet (hexdump with ascii view):
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

## .SC2
SCene file v2, smallest file, contains scene information and references to resources like textures. Similar to its' `.scg` counterpart in format.
### Header
The file seems to start with "SFV2)", `53 46 56 32 29` and contains a small header of 7 bytes.
### Blobs
Like `.scg`, the file is seperated into multiple sections, "blobs", which are of different lengths and seperated by the string "KA" (`4b 41`). Unlike `.scg` there are a few different key/value pairs and seemingly empty blobs which contain no key/value pairs. Each blob likely lines up with a counterpart in `.scg` and the empty blobs likely signify there is no information for the `.scg` blob at that index. Before any key/value pairs, there is a small 8 byte header after each `KA`.

Key/value pairs in order of appearance:
Key | Value
----|------
`##name`            | 2 bytes
`#dataNodes`        | 2 bytes
`#heirarchy`        | 2 bytes
`#id`               | 2 bytes
`#sceneComponents`  | varying length
