# Primitives

Common primitives that all file formats share.

## Vectors

```cpp
struct Vector2 {
  float components[2];
}
struct Vector3 {
  float components[3];
}
struct Vector4 {
  float components[4];
}
```

## Matrices

```cpp
struct Matrix2
  Vector2 components[2];
}
struct Matrix3
  Vector3 components[3];
}
struct Matrix4
  Vector4 components[4];
}
```
