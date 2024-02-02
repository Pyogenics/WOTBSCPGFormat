# SC2

Assembles the corresponding `scg` file's polygon groups into a meaningful hierarchy and properties.

```cpp
struct SC2 {
  SC2Header header;
  SC2VersionTags versionTags;
  SC2Descriptor descriptor;
  SC2Body body;
}
```

## Header

```cpp
struct SC2Header {
  ascii[4] magic;
  uint32 version;
  uint32 nodeCount;
}
```

## Version tags

TODO

```cpp
struct SC2VersionTags {
  KA tags;
}
```

## Descriptor

This documentation is incomplete. We do not know what properties this contains.

```cpp
struct SC2Descriptor {
  uint32 size;
  byte[size] data;
}
```

## Body

```cpp
struct SC2Body {
  KA body;
}
```

### Body format

```ts
interface SC2 {
  "#dataNodes": DataNode[];
  "#hierarchy": Hierarchy[];
  "#sceneComponents": SceneComponents;
}
```

#### Data nodes

- Name: always "NMaterial".
- Id: can be interpreted as `uint64`.
- Material name: a human readable name for the material
- Parent material key: if present, the parent material should be assigned to the mesh accessing this material.
- Quality group: what type of settings affects this material.
  - Example: "tank" or "terrain"
- Effects node: TODO
- Textures: TODO
- Config count: if present, it implies the present of config archive members

```ts
interface DataNode {
  '##name': 'NMaterial';
  '#id': Buffer;
  materialName: string;
  parentMaterialKey?: bigint;
  qualityGroup?: string;
  fxName?: string;
  textures?: Textures;
  configCount? number;
}
```
