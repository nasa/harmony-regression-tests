from harmony import BBox, Collection
import copy

non_production_configuration = {
    "single_output_tests": {
        "subset_bounding_box": {
            "SPL2SMA": {
                "request_params": {
                    "collection": Collection(id="C1242631429-NSIDC_CUAT"),
                    "granule_name": "SMAP_L2_SM_A_01063_D_20150414T061416_R13080_001.h5",
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
                    "granule_name": "SMAP_L3_FT_P_E_20231212_R19240_001.h5",
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
                    "granule_name": "SMAP_L2_SM_A_01063_D_20150414T061416_R13080_001.h5",
                    "shape": "ancillary/France_simple.geojson",
                    "labels": ["smap-rtest-2", "smap-rtests"],
                },
                "test_params": {"ext": ".h5"},
            },
        },
        "subset_by_shapefile": {
            "SPL3FTP": {
                "request_params": {
                    "collection": Collection(id="C1263071065-NSIDC_CUAT"),
                    "granule_name": "SMAP_L3_FT_P_20231212_R19240_001.h5",
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
                    "granule_name": "SMAP_L2_SM_P_E_47223_A_20231204T105336_R19240_001.h5",
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
            "SPL3SMA": {
                "request_params": {
                    "collection": Collection(id="C1242581633-NSIDC_CUAT"),
                    "granule_name": "SMAP_L3_SM_A_20150423_R13080_001.h5",
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
                    "granule_name": "SMAP_L3_SM_P_20231212_R19240_001.h5",
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
                    "granule_name": "SMAP_L4_C_mdl_20150401T000000_Vv8020_001.h5",
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
                    "granule_name": "SMAP_L2_SM_P_47226_A_20231204T154857_R19240_001.h5",
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


## run the same tests with Different Production values for Collection and GranuleID
production_overrides = {
    ("single_output_tests", "subset_bounding_box", "SPL2SMA"): {
        "collection": Collection(id="C2812935277-NSIDC_CPRD"),
    },
    ("single_output_tests", "subset_bounding_box", "SPL3FTP_E"): {
        "collection": Collection(id="C2938664439-NSIDC_CPRD"),
    },
    ("single_output_tests", "subset_by_geojson", "SPL2SMA"): {
        "collection": Collection(id="C2812935277-NSIDC_CPRD"),
    },
    ("single_output_tests", "subset_by_shapefile", "SPL3FTP"): {
        "collection": Collection(id="C2938664170-NSIDC_CPRD"),
    },
    ("single_output_tests", "subset_by_variable", "SPL2SMP_E"): {
        "collection": Collection(id="C2938663676-NSIDC_CPRD"),
    },
    ("single_output_tests", "subset_by_variable", "SPL3SMA"): {
        "collection": Collection(id="C2872766452-NSIDC_CPRD"),
    },
    ("single_output_tests", "subset_by_kml", "SPL3SMP"): {
        "collection": Collection(id="C2938664585-NSIDC_CPRD"),
    },
    ("single_output_tests", "reprojection_to_geographic", "SPL4CMDL"): {
        "collection": Collection(id="C3480440454-NSIDC_CPRD"),
    },
    ("multiple_output_tests", "GeoTIFF_reformat", "SPL2SMP"): {
        "collection": Collection(id="C2938663609-NSIDC_CPRD"),
    },
}


def _update_config_with_prod_values(in_config):
    """Return a production configuration.

    Make a copy of the input configuration and replace the collection and
    granule ID with production values.

    """
    out_config = copy.deepcopy(in_config)

    for (test_suite, test_type, short_name), p_config in production_overrides.items():
        out_config[test_suite][test_type][short_name]["request_params"][
            "collection"
        ] = p_config["collection"]
    return out_config


production_configuration = _update_config_with_prod_values(non_production_configuration)
