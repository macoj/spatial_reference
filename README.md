# spatial_reference
Sometimes I need to search an EPSG from ```spatialreferece.org```.

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
```
which returns:
```bash
[EPSG:2269] 100% hit
[EPSG:2913] 100% hit
[EPSG:3646] 100% hit
[EPSG:2270] 0% hit
[EPSG:2838] 0% hit
[EPSG:2839] 0% hit
```
This function tries to figure out the projection of these points by trying all the projections with "Oregon" in their description in ```spatialreferece.org``` then checks if the transformed points fall within the bounding box of Oregon with a known projection.

Other examples:
```python
# some points in Dallas
points = [(2514332.03903053, 7018364.6881987797), (2503623.9508441598, 6974201.6616298398), (2499328.3021238302, 6939465.4717225898), (2499328.3021238302, 6939465.4717225898), (2499328.3021238302, 6939465.4717225898)]
epsgs = SpatialReference.guess_the_projection(points, state="Texas")
for epsg, hits in epsgs[:5]:
    print "[EPSG:%d] %.0f%% hit" % (epsg, float(hits)/len(points)*100.0)
```

```bash
[EPSG:2276] 100% hit
[EPSG:2917] 100% hit
[EPSG:3670] 100% hit
[EPSG:2275] 0% hit
[EPSG:2277] 0% hit
```

```python
# some points in St. Louis:
points = [(894672.5, 995003.69999999995), (900456.30000000005, 1017035.0), (900456.30000000005, 1017035.0), (882164.59999999998, 999102.19999999995), (891889.30000000005, 1034635.0), (898334.0, 1022420.0), (894343.0, 1005425.0), (893510.30000000005, 1033772.0), (883747.80000000005, 1004093.0), (877404.59999999998, 1027557.0)]
epsgs = SpatialReference.guess_the_projection(points, state="Missouri")
for epsg, hits in epsgs[:5]:
    print "[EPSG:%d] %.0f%% hit" % (epsg, float(hits)/len(points)*100.0)
```

```bash
[EPSG:26797] 100% hit
[EPSG:26798] 100% hit
[EPSG:26796] 80% hit
[EPSG:2815] 0% hit
[EPSG:2816] 0% hit
```