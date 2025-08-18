from harmony import BBox, Collection

non_production_configuration = {
    "subset_bounding_box": {
        # Test 1 - Generates a single GeoTIFF.
        "SPL2SMA": {
            "request_params": {
                "collection": Collection(id="C1242631429-NSIDC_CUAT"),
                "granule_id": "G1260377350-NSIDC_CUAT",
                "spatial": BBox(-8.2, 42.0, 12.7, 52.8),
                "variables": ["Radar_Data/sigma0_hh_mean"],
                "format": "image/tiff",
                "labels": ["smap-test-1"],
            },
            "test_params": {"ext": "tif"},
        },
        # Test 7
        # Test 12 + variable
        # *** Test 15 + variable ***
        "SPL3FTP_E": {
            "request_params": {
                "collection": Collection(id="C1263071066-NSIDC_CUAT"),
                "granule_id": "G1263078049-NSIDC_CUAT",
                "spatial": BBox(-26, 63, -12, 67),
                "variables": [
                    "Freeze_Thaw_Retrieval_Data_Polar/freeze_thaw",
                    "Freeze_Thaw_Retrieval_Data_Polar/latitude",
                    "Freeze_Thaw_Retrieval_Data_Polar/longitude",
                ],
                "labels": ["smap-test-15"],
            },
            "test_params": {"ext": "nc4"},
        },
        # Test 17
        # Test 20
    },
    "subset_by_geojson": {
        # TEST 2
        # TEST 19
        # TEST 22
    },
    "subset_by_shapefile": {
        # TEST 3
        # TEST 4
        # TEST 13 +var
        # TEST 23
    },
    "subset_by_variable": {
        # TEST 5
        # TEST 6
        # *** TEST 10 ***
        "SPL2SMP_E": {
            "request_params": {
                "collection": Collection(id="C1263071064-NSIDC_CUAT"),
                "granule_id": "G1273163898-NSIDC_CUAT",
                "variables": [
                    "Soil_Moisture_Retrieval_Data/latitude",
                    "Soil_Moisture_Retrieval_Data/longitude",
                    "Soil_Moisture_Retrieval_Data/soil_moisture",
                    "Soil_Moisture_Retrieval_Data/soil_moisture_error",
                    "Soil_Moisture_Retrieval_Data_Polar/latitude",
                    "Soil_Moisture_Retrieval_Data_Polar/longitude",
                    "Soil_Moisture_Retrieval_Data_Polar/tb_h_corrected",
                    "Soil_Moisture_Retrieval_Data_Polar/tb_h_uncorrected",
                ],
                "labels": ["smap-test-10"],
            },
            "test_params": {"ext": "h5"},
        },
        # TEST 11 + reformat geotiff
        # *** TEST 16 ***
        "SPL2SMP_E_2": {
            "request_params": {
                "collection": Collection(id="C1242581633-NSIDC_CUAT"),
                "granule_id": "G1260703508-NSIDC_CUAT",
                "variables": ["Soil_Moisture_Retrieval_Data/soil_moisture"],
                "format": "image/tiff",
                "labels": ["smap-test-16"],
            },
            "test_params": {"ext": "tif"},
        },
        # TEST 24
    },
    "GeoTIFF_reformat": {
        # *** TEST 8 *** (generates a ton of GeoTIFFs. :grimmace: TODO [MHS, 08/15/2025] )
        # "SPL2SMP": {
        #     "request_params": {
        #         "collection": Collection(id="C1263071063-NSIDC_CUAT"),
        #         "granule_id": "G1273158728-NSIDC_CUAT",
        #         "format": "image/tiff",
        #     },
        #     "test_params": {"ext": "tif"},
        #     "labels": ["smap-test-8"],
        # },
        # TEST 14
    },
    "subset_by_kml": {
        # TEST 9
        # *** TEST 18 + reprojection ***
        "SPL3SMP": {
            "request_params": {
                "collection": Collection(id="C1263071067-NSIDC_CUAT"),
                "granule_id": "G1263078590-NSIDC_CUAT",
                "crs": "EPSG:4326",
                "shape": "ancillary/EasternUS.kml",
                "labels": ["smap-test-18"],
            },
            "test_params": {"ext": "nc4"},
        }
    },
    "reprojection_to_geographic": {
        # *** Test 21 ***
        "SPL4CMDL": {
            "request_params": {
                "collection": Collection(id="C1273193292-NSIDC_CUAT"),
                "granule_id": "G1273435798-NSIDC_CUAT",
                "crs": "EPSG:4326",
                "labels": ["smap-test-21"],
            },
            "test_params": {"ext": "nc4"},
        }
    },
}
