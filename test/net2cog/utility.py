"""Simple utility functions used in the net2cog test notebook."""

from os.path import basename
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import matplotlib.pyplot as plt
import rasterio
from harmony import Client
from numpy.testing import assert_array_almost_equal
from shared_utils import print_success, verify_cog_crs


def validate_smap_outputs(
    harmony_client: Client, harmony_job_id: str, expected_results: dict[str, Any]
):
    """Helper function to retrieve outputs from Harmony request and compare to reference
    metadata and files.

    Checks:

    * The expected number of files are returned.
    * The output files are valid Cloud Optimized GeoTIFFs.
    * The data values and metadata match a reference file.
    * The expected CRS value and output file CRS match.

    """
    harmony_client.wait_for_processing(harmony_job_id, show_progress=True)

    with TemporaryDirectory() as temp_dir:
        downloaded_cog_outputs = [
            file_future.result()
            for file_future in harmony_client.download_all(
                harmony_job_id, overwrite=True, directory=temp_dir
            )
        ]
        assert len(downloaded_cog_outputs) == expected_results["expected_file_count"]
        print_success(
            f"Correct number of generated output files: {expected_results['expected_file_count']}"
        )

        if expected_results.get("expected_file_substrings"):
            missing_substrings = [
                sub_string
                for sub_string in expected_results["expected_file_substrings"]
                if not any(
                    sub_string in cog_output for cog_output in downloaded_cog_outputs
                )
            ]
            assert (
                not missing_substrings
            ), f"Substrings {missing_substrings} not found in {downloaded_cog_outputs}"
            print_success(
                f"Correct output file substrings found: {expected_results['expected_file_substrings']}"
            )

        for downloaded_cog_file in downloaded_cog_outputs:
            verify_cog_crs(downloaded_cog_file, expected_results["expected_crs"], True)

            reference_file = Path(
                "./reference_data",
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
            ), f"output has incorrect metadata: {test_dataset.meta}"
            print_success("Generated image has correct metadata.")

            ref_image = reference_dataset.read()
            test_image = test_dataset.read()
            assert_array_almost_equal(ref_image, test_image)

    print_success("Generated image contains correct data.")


def validate_bounding_box_and_plot_cog_file(
    cog_file: str, expected_results: dict[str, Any]
) -> None:
    """Helper function to open, validate the bounding box, and plot the COG file.

    Checks:

    * The bounding box value in the output file is identical to the expected bounding box

    """
    with rasterio.open(cog_file) as src:
        raster_data = src.read(1)  # Read the first band

        expected_bboxs = expected_results["expected_bounding_box"]
        assert (
            src.bounds in expected_bboxs
        ), f"Bounds did not match: Expected {expected_bboxs}, got {src.bounds}"
        print_success(f"Correct Bounding Box: {src.bounds}")

        extent = (
            float(src.bounds.left),
            float(src.bounds.right),
            float(src.bounds.bottom),
            float(src.bounds.top),
        )

        # If src.bounds.bottom > src.bounds.top, the graph will be inverted.
        # When origin='lower' is used, the vertical axis points upward,
        # ensuring a correctly oriented graph
        if src.bounds.bottom > src.bounds.top:
            plt.imshow(raster_data, extent=extent, origin="lower")
        else:
            plt.imshow(raster_data, extent=extent)

        plt.title(f"{basename(cog_file)}")
        plt.show()
        print(f"{basename(cog_file)}: {src.bounds}\n")
