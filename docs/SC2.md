# SC2

Assembles the corresponding `scg` file's polygon groups into a meaningful hierarchy of nodes and properties.

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

It is unknown how this works and does not seem to affect the model.

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

- Name: always `"NMaterial"`.
- Id: can be interpreted as `uint64`.
- Material name: a human readable name for the material
- Parent material key: if present, the parent material should be assigned to the mesh accessing this material.
- Quality group: what type of settings affects this material.
  - Example: "tank" or "terrain"
- Effects node: it is unknown how this works.
- Textures: contains physically based rendering related textures
  - Albedo: color map
  - Base color map
    - R, G, B: standard colors
    - Alpha: secularity
  - Base normal map:
    - G is x and alpha is y
    - Use equation `z = sqrt(1 - x ** 2 - y ** 2)` to get z
  - Base roughness metallic map:
    - G: roughness
    - Alpha: metallicness
  - Decal mask: alpha mask for camouflages
  - Mask map: it is unknown what this does
  - Miscellaneous map:
    - G: ambient occlusion
    - Alpha: emissive
  - Normal map: regular DX11 style normal map
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

interface Textures {
  albedo: string;
  baseColorMap?: string;
  baseNormalMap?: string;
  baseRMMap?: string;
  decalmask?: string;
  maskMap?: string;
  miscMap?: string;
  normalmap?: string;
}
```
