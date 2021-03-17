import numpy
from osgeo import gdal
import os
# From https://gis.stackexchange.com/questions/111954/raster-diff-how-to-check-if-images-have-identical-values

def compare_images(reference, product):
    path = 'reference_images/'
    raster1 = path + reference
    raster2 = product

    ds1 = gdal.Open(raster1)
    ds2 = gdal.Open(raster2)

    r1 = numpy.array(ds1.ReadAsArray())
    r2 = numpy.array(ds2.ReadAsArray())

    d = numpy.array_equal(r1,r2)
    
    return(d)
    #if d == False:
    #    print("They differ")

    #else:
    #    print("They are the same")
