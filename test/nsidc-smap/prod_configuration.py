from harmony import BBox, Collection

production_configuration = {
    'subset_bounding_box': {
        # Test 1
        'SPL2SMA': {
            'collection_concept_id': Collection(id='xxxx-NSIDC_PROD'),
            'granule_id': 'xxx-NSIDC_PROD',
            'spatial': BBox(-8.2, 42.0, 12.7, 52.8),
            'variable': 'Radar_Data/sigma0_hh_mean',
            'format': 'image/tiff',
        }
        # Test 7
        # Test 12 + variable
        # *** Test 15 + variable ***
        # Test 17
        # Test 20
    },
    'subset_by_geojson': {
        # TEST 2
        # TEST 19
        # TEST 22
    },
    'subset_by_shapefile': {
        # TEST 3
        # TEST 4
        # TEST 13 +var
        # TEST 23
    },
    'subset_by_variable': {
        # TEST 5
        # TEST 6
        # *** TEST 10 ***
        # TEST 11 + reformat geotiff
        # *** TEST 16 ***
        # TEST 24
    },
    'GeoTIFF_reformat': {
        # *** TEST 8 ***
        # TEST 14
    },
    'subset_by_kml': {
        # TEST 9
        # *** TEST 18 + reprojection ***
    },
    'reprojection_to_geographic': {
        # *** TEST 21 ***
    },
}
