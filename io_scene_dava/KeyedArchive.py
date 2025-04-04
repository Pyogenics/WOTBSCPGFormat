from .Utils import unpackStream

class KeyedArchiveDataTypes:
    NONE = 0
    BOOLEAN = 1
    INT32 = 2
    FLOAT = 3
    STRING = 4
    WIDE_STRING = 5
    BYTE_ARRAY = 6
    UINT32 = 7
    KEYED_ARCHIVE = 8
    INT64 = 9
    UINT64 = 10
    VECTOR2 = 11
    VECTOR3 = 12
    VECTOR4 = 13
    MATRIX2 = 14
    MATRIX3 = 15
    MATRIX4 = 16
    COLOR = 17
    FASTNAME = 18
    AABBOX3 = 19
    FILEPATH = 20
    FLOAT64 = 21
    INT8 = 22
    UINT8 = 23
    INT16 = 24
    UINT16 = 25
    ARRAY = 27

'''
Version 1
'''
def readVersion1Value(stream):
    dataType, = unpackStream("B", stream)
    if dataType == KeyedArchiveDataTypes.NONE:
        return None
    elif dataType == KeyedArchiveDataTypes.BOOLEAN:
        value, = unpackStream("b", stream)
        return value > 0
    elif dataType == KeyedArchiveDataTypes.INT32:
        value, = unpackStream("<i", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.FLOAT:
        value, = unpackStream("<f", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.STRING:
        length, = unpackStream("<I", stream)
        value = stream.read(length).decode("utf-8")
        return value
    elif dataType == KeyedArchiveDataTypes.WIDE_STRING:
        length, = unpackStream("<I", stream)
        value = stream.read(length).decode("utf-16-le")
        return value
    elif dataType == KeyedArchiveDataTypes.BYTE_ARRAY:
        length, = unpackStream("<I", stream)
        value = stream.read(length)
        return value
    elif dataType == KeyedArchiveDataTypes.UINT32:
        value, = unpackStream("<I", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.KEYED_ARCHIVE:
        value = readKeyedArchive(stream)
        return value
    elif dataType == KeyedArchiveDataTypes.INT64:
        value, = unpackStream("<l", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.UINT64:
        value, = unpackStream("<L", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.VECTOR2:
        value = unpackStream("<2f", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.VECTOR3:
        value = unpackStream("<3f", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.VECTOR4:
        value = unpackStream("<4f", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.MATRIX2:
        value = unpackStream("<4f", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.MATRIX3:
        value = unpackStream("<9f", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.MATRIX4:
        value = unpackStream("<16f", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.COLOR:
        value = unpackStream("<4f", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.FASTNAME:
        #XXX: Version 1 shouldn't have fastnames?
        return None
    elif dataType == KeyedArchiveDataTypes.AABBOX3:
        value = unpackStream("<6f", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.FILEPATH:
        length, = unpackStream("<I", stream)
        value = stream.read(length).decode("utf-8")
        return value
    elif dataType == KeyedArchiveDataTypes.FLOAT64:
        value, = unpackStream("<d", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.INT8:
        value, = unpackStream("b", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.UINT8:
        value, = unpackStream("B", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.INT16:
        value, = unpackStream("<h", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.UINT16:
        value, = unpackStream("<H", stream)
        return value
    elif dataType == KeyedArchiveDataTypes.ARRAY:
        length, = unpackStream("<I", stream)
        value = []
        for _ in range(length):
            value.append(
                readVersion1Value(steam)
            )
        return value
    else:
        raise RuntimeError(f"Unknown KeyedArchive data type: {dataType}")

'''
Main IO
'''
def readKeyedArchive(stream):
    # Verify signature
    signature = stream.read(2)
    if signature != b"KA":
        raise RuntimeError(f"Invalid KeyedArchive signature: {signature}")
    
    # Read info
    version, versionVariant, childCount = unpackStream("<2BI", stream)
    
    # Read version specific data
    archive = {}
    if version == 1:
        for _ in range(childCount):
            key = readVersion1Value(stream)
            value = readVersion1Value(stream)
            archive[key] = value
    else:
        raise RuntimeError(f"Only version 1 KeyedArchives are implemented, got: {version}")

    print(f"[KeyedArchive version={version} variant={versionVariant} children={childCount}]")
    return archive