# .SC2
SCene file v2, smallest file, contains scene information and references to resources like textures.
## Header
The file starts with "SFV2" (magic: `53 46 56 32`) and contains a small header of 8 bytes made up of version and node count. This is followed by a KA containing "version tags", file descriptor and data node count. The header is followed by keyed archives.
```c
struct SC2Header
{
    uint32_t version;
    uint32_t nodeCount;
}
```
### Version tags
Contains version information todo with the scene file.
### Descriptor
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
