# Keyed Archive
Keyed archives are binary blobs stored inside both `.sc2` and `.scg` files that are used to store key/value pairs. Each keyed archive is identified with the magic "KA" (`4b 41`) and contains a small header, key/value pairs come directly after the header.

## Header
```c
struct KAHeader
{
    uint16_t version;
    uint32_t itemCount;
}
```

## Version 1
Each entry in a version 1 KA is identified by a 1 byte data type followed by the actual data, the data is read based on its' data type.
```c
struct KAEntry_v1
{
    uint8_t dataType;
    uint8_t data[];
}
```
### Data types
```c++
enum KATypes_v1 : uint8_t
{
    TYPE_NONE = 0,
    TYPE_BOOLEAN = 1,
    TYPE_INT32 = 2,
    TYPE_FLOAT = 3,
    TYPE_STRING = 4,
    TYPE_WIDE_STRING = 5,
    TYPE_BYTE_ARRAY = 6,
    TYPE_UINT32 = 7,
    TYPE_KEYED_ARCHIVE = 8,
    TYPE_INT64 = 9,
    TYPE_UINT64 = 10,
    TYPE_VECTOR2 = 11,
    TYPE_VECTOR3 = 12,
    TYPE_VECTOR4 = 13,
    TYPE_MATRIX2 = 14,
    TYPE_MATRIX3 = 15,
    TYPE_MATRIX4 16,
    TYPE_COLOR = 17,
    TYPE_FASTNAME = 18,
    TYPE_AABBOX3 = 19,
    TYPE_FILEPATH = 20,
    TYPE_FLOAT64 = 21,
    TYPE_INT8 = 22,
    TYPE_UINT8 = 23,
    TYPE_INT16 = 24,
    TYPE_UINT16 = 25,
    TYPES_COUNT = 26
};
```
All data types can be read raw with only a few exceptions.
#### none
Shouldn't exist inside a normal KA, this value is only used in code as a default value.
#### string, filepath, fastname
```c
struct KAstring_v1
{
    uint32_t length;
    char string[];
}
```
#### wide string
```c
struct KAwstring_v1
{
    uint32_t length;
    wchar_t string[];
}
```
#### byte array
```c
struct KAbytearray_v1
{
    uint32_t length;
    byte bytes[];
}
```
#### keyed archive
```c
struct KAkeyedarchive_v1
{
    uint32_t length;
    KA_v1 keyedArchive; // Nested KA
}
```

## Version 2
Only seen inside `.sc2` files; data seems to be packed tightly together compared to version 1.

Starts with an array of keys/values with the format.
```c
struct KAStringTableEntry_v2
{
    uint16_t length;
    char string[];
}
```
This is followed by an array of `uint32_t`s which are indices that map other KAs in the `.sc2` file to the string table.

## Version 258
Only seen inside `.sc2` files; the file is a series of back to back `uint32_t` key/value pairs which map into a string table stored inside a version 2 KA.
```c
struct KAEntry_v258
{
    uint32_t keyIndex;
    uint32_t valueIndex;
}
```
