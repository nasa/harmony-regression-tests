"""Simple utility functions used in the net2cog test notebook."""

from os.path import basename
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess

from harmony import Client
from numpy.testing import assert_array_almost_equal
from rasterio.crs import CRS
from rasterio.transform import Affine
import rasterio


def print_error(error_string: str) -> str:
    """Print an error, with formatting for red text."""
    print(f'\033[91m{error_string}\033[0m')


def print_success(success_string: str) -> str:
    """Print a success message, with formatting for green text."""
    print(f'\033[92mSuccess: {success_string}\033[0m')


def validate_smap_outputs(
    harmony_client: Client, harmony_job_id: str, expected_file_count: int
):
    """Helper function to retrieve outputs from Harmony request and compare to reference
    metadata and files.

    Checks:

    * The expected number of files are returned.
    * The output files are valid Cloud Optimized GeoTIFFs.
    * The data values and metadata match a reference file.

    """
    with TemporaryDirectory() as temp_dir:
        downloaded_cog_outputs = [
            file_future.result()
            for file_future in harmony_client.download_all(
                harmony_job_id, overwrite=True, directory=temp_dir
            )
        ]
        assert len(downloaded_cog_outputs) == expected_file_count
        print_success('Correct number of generated output files.')

        for cog_file in downloaded_cog_outputs:
            print(f'Assessing: {basename(cog_file)}')
            validate_cog(cog_file)

            expected_metadata = {
                'driver': 'GTiff',
                'dtype': get_expected_smap_dtype(cog_file),
                'nodata': get_expected_smap_nodata(cog_file),
                'width': 1440,
                'height': 720,
                'count': 1,
                'crs': CRS.from_epsg(4326),
                'transform': Affine(0.25, 0.0, 0.0, 0.0, 0.25, -90.0),
            }
            reference_file = Path(
                './reference_data',
                basename(cog_file),
            )

            assert_dataset_produced_correct_results(
                cog_file, expected_metadata, reference_file
            )


def get_expected_smap_dtype(cog_file_name: str) -> str:
    """Retrieve expected dtype for the COG metadata based on which
    variable is being tested. The default value is 'float32', but
    nobs and nobs_40km are 'int32' variables.

    """
    if 'nobs' in cog_file_name:
        expected_dtype = 'int32'
    else:
        expected_dtype = 'float32'

    return expected_dtype


def get_expected_smap_nodata(cog_file_name: str) -> float:
    """Retrieve expected nodata value for the COG metadata based on
    which variable is being tested. The default value is -9999.0, but
    nobs and nobs_40km have a nodata value of 0.0.

    """
    if 'nobs' in cog_file_name:
        expected_nodata = 0.0
    else:
        expected_nodata = -9999.0

    return expected_nodata


def assert_dataset_produced_correct_results(
    generated_file: Path, expected_metadata: dict, reference_file: Path
) -> None:
    """Check that the generated data matches the expected data."""
    with rasterio.open(generated_file) as test_dataset:
        assert (
            test_dataset.meta == expected_metadata
        ), f'output has incorrect metadata: {test_dataset.meta}'
        print_success('Generated image has correct metadata.')

        with rasterio.open(reference_file) as reference_dataset:
            ref_image = reference_dataset.read()
            test_image = test_dataset.read()
            assert_array_almost_equal(ref_image, test_image)

    print_success('Generated image contains correct data.')


def validate_cog(path: Path) -> None:
    cogtif_val = ['rio', 'cogeo', 'validate', f'{path}']

    process = subprocess.run(
        cogtif_val, check=True, stdout=subprocess.PIPE, universal_newlines=True
    )
    cog_test = process.stdout
    cog_test = cog_test.replace("\n", "")

    valid_cog = f"{path} is a valid cloud optimized GeoTIFF"
    assert cog_test == valid_cog
