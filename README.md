# py-lenses
Experimental lens like library in Python

Goals:
- reusability and composition of lenses
- typesafe
- easy syntax

Example of a composed lens using the overloaded `>>` operator

```python
    data = {"x": {"y": 42}}

    lens_x = DictLens[dict](key="x")
    lens_y = DictLens[int](key="y")

    lens = lens_x >> lens_y

    error, result = lens(data)

    assert result == 42
```
