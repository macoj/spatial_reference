# spatial_reference
Sometimes I need to search an EPSG from spatialreferece.org.


```python
execfile("spatial_reference.py")
print SpatialReference.epsg_search("Florida West")
[('26759', 'NAD27 / Florida West'), ('26959', 'NAD83 / Florida West')]
```

#TODO
Let's say that I have a set of points of a city, but I do not have any clue about the projection of such points. How to find the projection or at least a good guess?
