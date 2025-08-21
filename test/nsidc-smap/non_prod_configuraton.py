from harmony import BBox, Collection

non_production_configuration = {
    "single_output_tests": {
        "subset_bounding_box": {
            "SPL2SMA": {
                "request_params": {
                    "collection": Collection(id="C1242631429-NSIDC_CUAT"),
                    "granule_id": "G1260377350-NSIDC_CUAT",
                    "spatial": BBox(-8.2, 42.0, 12.7, 52.8),
                    "variables": ["Radar_Data/sigma0_hh_mean"],
                    "format": "image/tiff",
                    "labels": ["smap-rtest-1", "smap-rtests"],
                },
                "test_params": {"ext": ".tif"},
            },
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
                    "labels": ["smap-rtest-15", "smap-rtests"],
                },
                "test_params": {"ext": ".nc4"},
            },
        },
        "subset_by_geojson": {
            "SPL2SMA": {
                "request_params": {
                    "collection": Collection(id="C1242631429-NSIDC_CUAT"),
                    "granule_id": "G1260377350-NSIDC_CUAT",
                    "labels": ["smap-rtest-2", "smap-rtests"],
                    "shape": "ancillary/France_simple.geojson",
                },
                "test_params": {"ext": ".h5"},
            },
        },
        "subset_by_shapefile": {
            "SPL3FTP": {
                "request_params": {
                    "collection": Collection(id="C1263071065-NSIDC_CUAT"),
                    "granule_id": "G1263076419-NSIDC_CUAT",
                    "variables": [
                        "Freeze_Thaw_Retrieval_Data_Polar/freeze_thaw",
                        "Freeze_Thaw_Retrieval_Data_Polar/latitude",
                        "Freeze_Thaw_Retrieval_Data_Polar/longitude",
                        "Freeze_Thaw_Retrieval_Data_Polar/tbh_mean",
                    ],
                    "labels": ["smap-rtest-13", "smap-rtests"],
                    "shape": "ancillary/Semey.zip",
                },
                "test_params": {"ext": ".nc4"},
            },
        },
        "subset_by_variable": {
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
                    "labels": ["smap-rtest-10", "smap-rtests"],
                },
                "test_params": {"ext": ".h5"},
            },
            "SPL2SMP_E_2": {
                "request_params": {
                    "collection": Collection(id="C1242581633-NSIDC_CUAT"),
                    "granule_id": "G1260703508-NSIDC_CUAT",
                    "variables": ["Soil_Moisture_Retrieval_Data/soil_moisture"],
                    "format": "image/tiff",
                    "labels": ["smap-rtest-16", "smap-rtests"],
                },
                "test_params": {"ext": ".tif"},
            },
        },
        "subset_by_kml": {
            "SPL3SMP": {
                "request_params": {
                    "collection": Collection(id="C1263071067-NSIDC_CUAT"),
                    "granule_id": "G1263078590-NSIDC_CUAT",
                    "crs": "EPSG:4326",
                    "shape": "ancillary/EasternUS.kml",
                    "labels": ["smap-rtest-18", "smap-rtests"],
                },
                "test_params": {"ext": ".nc4"},
            }
        },
        "reprojection_to_geographic": {
            "SPL4CMDL": {
                "request_params": {
                    "collection": Collection(id="C1273193292-NSIDC_CUAT"),
                    "granule_id": "G1273435798-NSIDC_CUAT",
                    "crs": "EPSG:4326",
                    "labels": ["smap-rtest-21", "smap-rtests"],
                },
                "test_params": {"ext": ".nc4"},
            }
        },
    },
    "multiple_output_tests": {
        "GeoTIFF_reformat": {
            # *** TEST 8 *** (generates a ton of GeoTIFFs. :grimmace: TODO [MHS, 08/15/2025] )
            "SPL2SMP": {
                "request_params": {
                    "collection": Collection(id="C1263071063-NSIDC_CUAT"),
                    "granule_id": "G1273158728-NSIDC_CUAT",
                    "format": "image/tiff",
                    "variables": [
                        "Soil_Moisture_Retrieval_Data/EASE_column_index",
                        "Soil_Moisture_Retrieval_Data/EASE_row_index",
                        "Soil_Moisture_Retrieval_Data/albedo",
                        "Soil_Moisture_Retrieval_Data/albedo_option3",
                        "Soil_Moisture_Retrieval_Data/boresight_incidence",
                        "Soil_Moisture_Retrieval_Data/bulk_density",
                        "Soil_Moisture_Retrieval_Data/freeze_thaw_fraction",
                        "Soil_Moisture_Retrieval_Data/grid_surface_status",
                        "Soil_Moisture_Retrieval_Data/landcover_class_fraction",
                        "Soil_Moisture_Retrieval_Data/landcover_class",
                        "Soil_Moisture_Retrieval_Data/sand_fraction",
                        "Soil_Moisture_Retrieval_Data/soil_moisture",
                        "Soil_Moisture_Retrieval_Data/surface_flag",
                        "Soil_Moisture_Retrieval_Data/tb_4_corrected",
                        "Soil_Moisture_Retrieval_Data/tb_h_corrected",
                        "Soil_Moisture_Retrieval_Data/tb_h_uncorrected",
                        "Soil_Moisture_Retrieval_Data/tb_qual_flag_4",
                        "Soil_Moisture_Retrieval_Data/tb_qual_flag_h",
                        "Soil_Moisture_Retrieval_Data/tb_qual_flag_v",
                        "Soil_Moisture_Retrieval_Data/vegetation_opacity_option3",
                    ],
                    "labels": ["smap-rtest-8", "smap-rtests"],
                },
                "test_params": {"ext": ".tif"},
            },
        },
    },
}
