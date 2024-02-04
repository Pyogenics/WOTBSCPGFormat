# Keyed archive

Represents a tree of data.

```cpp
struct KA {
  KAHeader header;
  KABody body;
}
```

## Header

The header's version of the keyed archive determines what comes next.

```cpp
struct KAHeader {
  uint16 version;
}
```

## Body version `0x0001`

A very basic archive where any given child is a pair of a string (the key) and some value. Check below for documentation on `KAPair`.

```cpp
struct KABodyV0x0001 {
  uint32 count;
  KAPair[count] children;
}
```

## Body version `0x0002`

This archive leverages fast names (numeric ids pointing to a string in a table). This archive is structured as follows:

- Fast name count: the number of members in the string table.
- Fast names: an array of strings
- Fast name ids: an array of ids that correspond with the array of strings
  - Assemble names and ids into a table for later use by fast name keyed arhive values
  - The key of an archive pair here is also a fast name
- The children

```cpp
struct KABodyV0x0002 {
  uint32 fastNameCount;
  KAFastNameString[fastNameCount] fastNames;
  uint32[fastNameCount] fastNameIds;
  uint32 count;
  KABodyV0x0002Pair[count] children;
}

struct KAFastNameString {
  uint16 length;
  ascii[length] value;
}

struct KABodyV0x0002Pair {
  uint32 keyFastNameId;
  KAValue value;
}
```

## Body version `0x0102`

This keyed archive version can only be a (possibly indirect) descendant of a keyed archive version `0x0002` as it relies on a fast name string table. `value` should be treated just like a `KAValue` unless the `value`'s type is `KAType.STRING` in which case it should be treated like a fast name.

```cpp
struct KABodyV0x0102 {
  uint32 count;
  KABodyV0x0102Pair[count] children;
}

struct KABodyV0x0102Pair {
  KAValueBodyTypeFastName key;
  KABodyV0x0102PairValue value;
}
```

## Body version `0xff02`

This is completely empty.

```cpp
struct KABodyV0xff02 {}
```

## Primitives

These primitives can be found throughout the archive.

```cpp
struct KAPair {
  KAValue name; // always a string
  KAValue value;
}

struct KAValue {
  KAValueHeader header;
  KAValueBody body; // look below for documentation on this
}

struct KAValueHeader {
  KAType type; // read as uint8
}

enum KAType {
  NONE = 0,
  BOOLEAN = 1,
  INT32 = 2,
  FLOAT = 3,
  STRING = 4,
  WIDE_STRING = 5,
  BYTE_ARRAY = 6,
  UINT32 = 7,
  KEYED_ARCHIVE = 8,
  INT64 = 9,
  UINT64 = 10,
  VECTOR2 = 11,
  VECTOR3 = 12,
  VECTOR4 = 13,
  MATRIX2 = 14,
  MATRIX3 = 15,
  MATRIX4 = 16,
  COLOR = 17,
  FASTNAME = 18,
  AABBOX3 = 19,
  FILEPATH = 20,
  FLOAT64 = 21,
  INT8 = 22,
  UINT8 = 23,
  INT16 = 24,
  UINT16 = 25,
  ARRAY = 27,
  TRANSFORM = 29,
}
```

### Value bodies

What `KAValueBody` is depends on the header's `type`.

```cpp
struct KAValueBodyTypeNone {}
struct KAValueBodyTypeBoolean {
  bool value;
}
struct KAValueBodyTypeInt32 {
  int32 value;
}
struct KAValueBodyTypeFloat {
  float value;
}
struct KAValueBodyTypeString {
  uint32 length;
  ascii[length] value;
}
struct KAValueBodyTypeWideString {
  uint32 length;
  wchar_t[length] value;
}
struct KAValueBodyTypeByteArray {
  uint32 length;
  byte[length] value;
}
struct KAValueBodyTypeUint32 {
  uint32 value;
}
struct KAValueBodyTypeKeyedArchive {
  KA value;
}
struct KAValueBodyTypeInt64 {
  int64 value;
}
struct KAValueBodyTypeUint64 {
  uint64 value;
}
struct KAValueBodyTypeVector2 {
  Vector2 value;
}
struct KAValueBodyTypeVector3 {
  Vector3 value;
}
struct KAValueBodyTypeVector4 {
  Vector4 value;
}
struct KAValueBodyTypeMatrix2 {
  Matrix2 value;
}
struct KAValueBodyTypeMatrix3 {
  Matrix3 value;
}
struct KAValueBodyTypeMatrix4 {
  Matrix4 value;
}
struct KAValueBodyTypeColor {
  // it is unknown how this works
}
struct KAValueBodyTypeFastName {
  uint32 index;
  // value is the index member of corresponding string table
}
struct KAValueBodyTypeAABBox3 {
  Vector3 minimum;
  Vector3 maximum;
}
struct KAValueBodyTypeFilePath {
  uint32 length;
  ascii[length] value;
}
struct KAValueBodyTypeFloat64 {
  double value;
}
struct KAValueBodyTypeInt8 {
  int8 value;
}
struct KAValueBodyTypeInt16 {
  int16 value;
}
struct KAValueBodyTypeUint16 {
  uint16 value;
}
struct KAValueBodyTypeArray {
  uint32 length;
  KAValue[length] values;
}
struct KAValueBodyTypeTransform {
  Vector3 position;
  Vector3 scale;
  Vector4 quaternion; // rotation
}
```
