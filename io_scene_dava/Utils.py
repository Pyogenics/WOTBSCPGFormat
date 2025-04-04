from struct import unpack, calcsize

def unpackStream(format, stream):
    dataSize = calcsize(format)
    data = unpack(format, stream.read(dataSize))
    return data