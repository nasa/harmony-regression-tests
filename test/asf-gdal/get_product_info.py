def get_product_info(collection, infile):
    from osgeo import gdal
    import osr
    from pyproj import Transformer
    ds = gdal.Open(infile)
    proj = osr.SpatialReference(wkt=ds.GetProjection())
    width = ds.RasterXSize
    height = ds.RasterYSize
    xy_size = [width, height]
    bands = ds.RasterCount
    meta = ds.GetMetadata()
    gt = ds.GetGeoTransform()
    minx = gt[0]
    miny = (gt[3] + width*gt[4] + height*gt[5])
    maxx = (gt[0] + width*gt[1] + height*gt[2])
    maxy = (gt[3])
    gcs = proj.GetAttrValue('GEOGCS',0)
    authority = proj.GetAttrValue('AUTHORITY',0)
    projcs = 'NA'
    proj_epsg = 'NA'
    if proj.IsProjected() == 1 and proj.IsGeographic() == 0:
        cs = 'Projected'
        projcs = proj.GetAttrValue('PROJCS',0)
        proj_epsg = proj.GetAttrValue("AUTHORITY", 1)
        gcs_epsg = proj.GetAttrValue("PROJCS|GEOGCS|AUTHORITY", 1)
        # Transform projected spatial extent to lat/long (WGS84 EPSG:4326)
        proj_string = 'epsg:' + proj_epsg
        inProj = proj_string
        outProj = 'epsg:4326'
        transformer = Transformer.from_crs(inProj, outProj)
        min_extent = transformer.transform(minx,miny)
        max_extent = transformer.transform(maxx,maxy)
        extent = [round(min_extent[0], 2), round(max_extent[0], 2),round(min_extent[1], 2), round(max_extent[1], 2)]
    elif proj.IsProjected() == 0 and proj.IsGeographic() ==1:
        cs = 'Geographic'
        gcs_epsg = proj.GetAttrValue("AUTHORITY", 1)
        extent = [round(miny,2), round(maxy,2),round(minx, 2), round(maxx, 2)]
    ds = None

    gdi = gdal.Info(infile)
    var_list = ['NA', 'NA', 'NA', 'NA']
    var_count = 0
    # GRFN
    if collection == 's1_insar':
        for item in gdi.split("\n"):
            if "NETCDF" in item:
                var_list[var_count] = item.strip().partition("=")[2]
                var_count += 1
    # UAVSAR
    elif collection == 'uavsar' or collection == 'avnir':
        for item in gdi.split("\n"):
            if "Description" in item:
                var_list[var_count] = item.strip().partition("= ")[2]
                var_count += 1
        if var_count == 0:
            for item in gdi.split("\n"):
                if "Block=" in item:
                    var_list[var_count] = item[0:4] + item[5]
                    var_count += 1
    gdi = None
    information = {'gdal_cs': cs,
                   'gdal_proj_cs': projcs,
                   'gdal_gcs': gcs,
                   'gdal_authority': authority,
                   'gdal_proj_epsg': proj_epsg,
                   'gdal_gcs_epsg': gcs_epsg,
                   'gdal_spatial_extent': extent,
                   'gdal_n_bands' : bands,
                   'gdal_xy_size' : xy_size,
                   'gdal_variables' : var_list}

    return(information)
