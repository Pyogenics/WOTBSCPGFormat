'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import bpy

bl_info = {
    name: "DAVASceneIO",
    description: "Support for DAVA framework scene files",
    author: "Pyogenics, https://www.github.com/Pyogenics",
    version: (1, 0, 0),
    blender: (3, 6, 0),
    doc_url: "https://github.com/Pyogenics/SCPG-reverse-engineering",
    tracker_url: "https://github.com/Pyogenics/SCPG-reverse-engineering/issues",
    category: "Import-Export"
}

'''
UI
'''

'''
Register
'''

def register():
    print("Hello, world!")

def unregister():
    print("Goodbye, cruel world!")

if __name__ == "__main__":
    register()
