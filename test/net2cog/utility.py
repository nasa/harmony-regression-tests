"""Simple utility functions used in the net2cog test notebook."""

from os.path import basename
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess

from harmony import Client
from numpy.testing import assert_array_almost_equal
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

        for downloaded_cog_file in downloaded_cog_outputs:
            print(f'Assessing: {basename(downloaded_cog_file)}')
            validate_cog(downloaded_cog_file)

            reference_file = Path(
                './reference_data',
                basename(downloaded_cog_file),
            )

            assert_dataset_produced_correct_results(downloaded_cog_file, reference_file)


def assert_dataset_produced_correct_results(
    generated_file: Path, reference_file: Path
) -> None:
    """Check that the generated data matches the expected data."""
    with rasterio.open(generated_file) as test_dataset:
        with rasterio.open(reference_file) as reference_dataset:
            assert (
                test_dataset.meta == reference_dataset.meta
            ), f'output has incorrect metadata: {test_dataset.meta}'
            print_success('Generated image has correct metadata.')

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
