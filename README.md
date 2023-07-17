# World Of Tanks: Blitz SCPG model format
Reverse engineered information about the model format used by WOTB.

## Preface
This resource aims to shed light on the model format, "SCPG", used by WOTB and eventually provide tools to modify and create said models. Wargaming poses tools to work with "SCPG" models however they are proprietary and not much is known about them in the community.

Models in WOTB are located in `/packs/3d/` and each model comes in a pair of files with extensions `.scg` and `.sc2`, for example: `packs/3d/Tanks/German/Maus.scg` `packs/3d/Tanks/German/Maus.sc2`. Game files are compressed using the `dvpl` format, you can use [this](https://github.com/Tankerch/DVPL_Converter) tool to decompress them.

## .SCG
### Header
The file starts with "SCPG", aka the magic `53 43 50 47` and contains a small header of 11 bytes.

Example: `53 43 50 47 01 00 00 00  53 00 00 00 53 00 00 00`
### Blobs
The file is seperated into multiple sections, "blobs", which are of different lengths and seperated by the string "KA" (`4b 41`).

Each blob contains a number of key/value pairs of varying length and seem to always appear in the same order, some values also seem to be the same length between blobs and files. Before the first key/value pair there is a small 11 byte header.

Key | Value
----|------
`##name`                | 5 bytes
`PolygonGroup`          | 5 bytes
`#id`                   | 18 bytes
`cubeTextureCoordCount` | 10 bytes
`indexFormat`           | 10 bytes
`indices`               | varying length
`packing`               | 10 bytes
`primitiveCount`        | 10 bytes
`rhi_primitiveType`     | 10 bytes
`textureCoordCount`     | 10 bytes
`vertexCount`           | 10 bytes
`vertexFormat`          | 10 bytes
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
