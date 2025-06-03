"""Simple utility functions used in the net2cog test notebook."""

from os.path import basename
from pathlib import Path
from tempfile import TemporaryDirectory

from harmony import Client
from numpy.testing import assert_array_almost_equal
from rio_cogeo.cogeo import cog_validate, cog_info
import rasterio
import matplotlib.pyplot as plt


def print_error(error_string: str) -> str:
    """Print an error, with formatting for red text."""
    print(f'\033[91m{error_string}\033[0m')


def print_success(success_string: str) -> str:
    """Print a success message, with formatting for green text."""
    print(f'\033[92mSuccess: {success_string}\033[0m')


def validate_smap_outputs(
    harmony_client: Client, harmony_job_id: str, expected_results: list
):
    """Helper function to retrieve outputs from Harmony request and compare to reference
    metadata and files.

    Checks:

    * The expected number of files are returned.
    * The output files are valid Cloud Optimized GeoTIFFs.
    * The data values and metadata match a reference file.
    * The expected CRS value and output file CRS match.

    """
    with TemporaryDirectory() as temp_dir:
        downloaded_cog_outputs = [
            file_future.result()
            for file_future in harmony_client.download_all(
                harmony_job_id, overwrite=True, directory=temp_dir
            )
        ]
        assert len(downloaded_cog_outputs) == expected_results['expected_file_count']
        print_success(
            'Correct number of generated output files: %d'
            % expected_results['expected_file_count']
        )

        for downloaded_cog_file in downloaded_cog_outputs:
            print(f'Assessing: {basename(downloaded_cog_file)}')

            # Verify output file is valid COG and CRS is correct
            assert cog_validate(downloaded_cog_file)[0]
            print_success('Generated output files is a valid COG.')

            assert (
                cog_info(downloaded_cog_file).GEO.CRS
                == expected_results['expected_crs']
            )
            print_success(
                'Correct Coordinate Reference System (CRS): %s'
                % cog_info(downloaded_cog_file).GEO.CRS
            )

            reference_file = Path(
                './reference_data',
                basename(downloaded_cog_file),
            )

            if reference_file.exists():
                assert_dataset_produced_correct_results(
                    downloaded_cog_file, reference_file
                )

            validate_bounding_box_and_plot_cog_file(
                downloaded_cog_file, expected_results
            )


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


def validate_bounding_box_and_plot_cog_file(
    cog_file: str, expected_results: list
) -> None:
    """Helper function to open, validate the bounding box, and plot the COG file.

    Checks:

    * The bounding box value in the output file is identical to the expected bounding box

    """
    with rasterio.open(cog_file) as src:
        raster_data = src.read(1)  # Read the first band

        assert src.bounds in expected_results['expected_bounding_box']
        print_success('Correct Bounding Box')

        extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]

        # Graph is inverted if src.bounds.bottom > src.bounds.top.
        # origin='lower', the [0, 0] index is placed at the lower-left
        # corner of the axes. The vertical axis points upwards.
        if src.bounds.bottom > src.bounds.top:
            plt.imshow(raster_data, extent=extent, origin='lower')
        else:
            plt.imshow(raster_data, extent=extent)

        plt.title(f'{basename(cog_file)}')
        plt.xticks([]), plt.yticks([])
        plt.show()
        print(f'{basename(cog_file)}: {src.bounds}\n')
