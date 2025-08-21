"""Collection of functions used for nsidc-smap regression tests."""

from earthdata_hashdiff import (
    create_geotiff_hash_file,
    create_nc4_hash_file,
    geotiff_matches_reference_hash_file,
    nc4_matches_reference_hash_file,
    h5_matches_reference_hash_file,
)
from pathlib import Path


def file_for_variable(directory: Path, glob: str) -> Path:
    """Return a Path to the matching single file.

    Find a file in a directory by a glob string.

    Raise error if mulitple files  match.
    """
    results = list(directory.glob(glob))
    if len(results) != 1:
        raise ValueError(f"Incorrect Number of files found ({len(results)}) for {glob}")

    return results[0]


def comparison_function_by_extension(ext: str) -> callable:
    """Returns the correct function to call for the input file type's extension."""

    compare_function_map = {
        ".tif": geotiff_matches_reference_hash_file,
        ".nc4": nc4_matches_reference_hash_file,
        ".h5": h5_matches_reference_hash_file,
    }
    return compare_function_map[ext]


def _generate_reference_files(test_config: dict, in_dir: Path, out_dir: Path):
    """Process downloaded output into hashed files to be used as reference.

    This routine is used to create the reference files for the the test.

    It's NOT used to run the test.

    Args:
        test_config: Dictionary containing test configuration with request parameters
        in_dir: Path to input directory containing downloaded data files
        out_dir: Path to output directory where reference files will be saved

    Example:
        from smap_utils import generate_reference_files
        from pathlib import Path

        in_dir = Path('temporary-directory/')
        out_dir = Path('reference_files/')

        from non_prod_configuraton import non_production_configuration

        generate_reference_files(non_production_configuration["multiple_output_tests"]["GeoTIFF_reformat"]["SPL2SMP"], in_dir, out_dir)

    """
    ## Generate reference files for the multifile request
    for full_var in test_config["request_params"]["variables"]:
        var = full_var.split("/")[-1]
        in_fn = file_for_variable(in_dir, f"*Data_{var}_reformatted*")
        out_fn = out_dir / f"{var}_reference.json"
        print(f"generating geohash for {in_fn}")
        create_geotiff_hash_file(str(in_fn), str(out_fn))

    ## generate for the single file tests
    input_files = [
        Path("SPL2SMA_subset_bounding_box.tif"),
        Path("SPL2SMA_subset_by_geojson.h5"),
        Path("SPL2SMP_E_2_subset_by_variable.tif"),
        Path("SPL2SMP_E_subset_by_variable.h5"),
        Path("SPL3FTP_E_subset_bounding_box.nc4"),
        Path("SPL3FTP_subset_by_shapefile.nc4"),
        Path("SPL3SMP_subset_by_kml.nc4"),
        Path("SPL4CMDL_reprojection_to_geographic.nc4"),
    ]
    for inbase in input_files:
        out_fn = out_dir / f"{inbase.stem}_reference.json"
        in_fn = in_dir / inbase
        print(f"generating geohash/hash for {in_fn}")
        if inbase.suffix == ".tif":
            create_geotiff_hash_file(str(in_fn), str(out_fn))
        else:
            create_nc4_hash_file(str(in_fn), str(out_fn))
