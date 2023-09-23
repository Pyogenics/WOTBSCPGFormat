'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from .KA import readKA1

'''
Errors
'''
class SCGReadError(RuntimeError): pass
class SCGWriteError(RuntimeError): pass

'''
SCG reader
'''
def readSCG(stream):
    if stream.readBytes(4) != B"SCPG":
        raise SCGReadError("Invalid magic string")

    version = stream.readInt32(False)
    nodeCount = stream.readInt32(False)
    stream.readInt32(False) #TODO: Duplicate node count field?

    polygonGroups = {}
    for _ in range(nodeCount):
        node = readKA1(stream)
        if node["##name"] != "PolygonGroup":
            print("Warning: SCG node wasn't a polygon group, skipping")
            continue
        polygonGroups[ int.from_bytes(node["#id"], "little") ] = node

    return polygonGroups

'''
SCG writer
'''
def writeScg(stream): pass
