# Primitives

Common primitives that all file formats share.

## Vectors

```cpp
struct Vector2 {
  float[2] components;
}
struct Vector3 {
  float[3] components;
}
struct Vector4 {
  float[4] components;
}
```

## Matrices

```cpp
struct Matrix2
  Vector2[2] components;
}
struct Matrix3
  Vector3[3] components;
}
struct Matrix4
  Vector4[4] components;
}
```
