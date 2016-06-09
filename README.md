# spatial_reference
Sometimes I need to search an EPSG from spatialreferece.org.

```python
execfile("spatial_reference.py")
print SpatialReference.epsg_search("Florida West")
[('26759', 'NAD27 / Florida West'), ('26959', 'NAD83 / Florida West')]
```

Also, sometimes I want to guess the projection of a set of points which I do not have any clue about it:
```python
execfile("spatial_reference.py")
points = [(7647409.02929, 686790.02595000004), (7647471.0159499999, 688344.44999999995),  (7645653.23905, 684826.79570999998), (7645656.2857100004, 684567.37809999997)]
epsgs = SpatialReference.guess_the_projection(points, state="Oregon")
for epsg, hits in epsgs[:5]:
    print "[EPSG:%d] %.0f%% hit" % (epsg, float(hits)/len(points)*100.0)
[EPSG:2269] 100% hit
[EPSG:2913] 100% hit
[EPSG:3646] 100% hit
[EPSG:2270] 0% hit
[EPSG:2838] 0% hit
[EPSG:2839] 0% hit
```