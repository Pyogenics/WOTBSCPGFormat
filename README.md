# World Of Tanks: Blitz SCPG model format

Reverse engineered information about the model format used by WOTB.

## Preface

This resource aims to shed light on the model format, "SCPG", used by WOTB and eventually provide tools to modify and create said models.

Models in WOTB are located in `/packs/3d/` and each model comes in a pair of files with extensions `.scg` and `.sc2`, for example: `packs/3d/Tanks/German/Maus.scg` `packs/3d/Tanks/German/Maus.sc2`. Game files are compressed using the `dvpl` format, you can use [this](https://github.com/Tankerch/DVPL_Converter) tool to decompress them.

Current work is based on SC2 version 41 and SCG version 1.

## Blender plugin

Read about it [here](blender/README.md)

## Research materials

An old version of the DAVA engine is available [here](https://github.com/smile4u/dava.engine).

- [KeyedArchive](https://github.com/smile4u/dava.engine/blob/development/Sources/Internal/FileSystem/KeyedArchive.cpp)
- [KeyedArchive data R/W](https://github.com/smile4u/dava.engine/blob/development/Sources/Internal/FileSystem/VariantType.cpp)
- [SceneFileV2](https://github.com/smile4u/dava.engine/blob/development/Sources/Internal/Scene3D/SceneFileV2.cpp)
- [PolygonGroup](https://github.com/smile4u/dava.engine/blob/development/Sources/Internal/Render/3D/PolygonGroup.cpp)
- [PolygonGroup vertex format RW](https://github.com/smile4u/dava.engine/blob/development/Sources/Internal/Render/3D/PolygonGroup.h)

[gmConverter3D](https://gamemodels3d.com/forum/?topic=1348) program for converting multiple model formats, including scg + sc2. Contains useful reference implementation of more recent versions of SC2 in javascript.

## File format documentation

Binary structures are represented as C++ struts and thr resulting tree is represented as TypeScript definitions. All values use little endian encoding.

- [Keyed archive](docs/KA.md)
- [Scene geometry](docs/SCG.md)
- [Scene version 2](docs/SC2.md)
- [Primitives](docs/primitives.md)
