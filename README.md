# spatial_reference
Sometimes I need to search an EPSG from spatialreferece.org.


```python
execfile("spatial_reference.py")
print SpatialReference.epsg_search("Florida West")
[('26759', 'NAD27 / Florida West'), ('26959', 'NAD83 / Florida West')]
```
