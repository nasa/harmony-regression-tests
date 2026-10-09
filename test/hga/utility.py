import hashlib
import json
from os.path import basename
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import rasterio
from harmony import Client
from numpy.testing import assert_array_almost_equal
from rio_cogeo.cogeo import cog_info

save_md5sums = True


def print_error(error_string: str) -> None:
    """Print an error, with formatting for red text."""
    print(f"\033[91m{error_string}\033[0m")


def print_success(success_string: str) -> None:
    """Print a success message, with formatting for green text."""
    print(f"\033[92mSuccess: {success_string}\033[0m")


def verify_cog_crs(downloaded_cog_file, expected_crs: str):
    """Verify output file is valid COG and CRS is correct"""
    print(f"Assessing: {basename(downloaded_cog_file)}")

    assert (
        cog_info(downloaded_cog_file).GEO.CRS == expected_crs
    ), f"Expected crs {expected_crs}, got {cog_info(downloaded_cog_file).GEO.CRS}"

    print_success(
        f"Correct Coordinate Reference System (CRS): {cog_info(downloaded_cog_file).GEO.CRS}"
    )


def validate_nisar_outputs(
    harmony_client: Client,
    harmony_job_id: str,
    expected_results: dict[str, Any],
    test_case,
    save_md5sums: bool = False,
):
    """Helper function to retrieve outputs from Harmony GCOV net2cog request and compare to reference
    metadata and files.

    Checks:

    * The expected number of files are returned.
    * The output files are valid Cloud Optimized GeoTIFFs.
    * The expected CRS value and output file CRS match.
    * The data's md5sum matches reference md5sum.

    """

    harmony_client.wait_for_processing(harmony_job_id)

    with TemporaryDirectory() as temp_dir:
        downloaded_cog_outputs = [
            Path(harmony_client.download(url, temp_dir).result())
            for url in harmony_client.result_urls(harmony_job_id)
            if not url.endswith(".txt")
        ]

        assert (
            len(downloaded_cog_outputs) == expected_results["expected_file_count"]
        ), f"Invalid output count expected {expected_results['expected_file_count']} got {len(downloaded_cog_outputs)}."
        print_success(
            f"Correct number of generated output files: {expected_results['expected_file_count']}"
        )

        for file in downloaded_cog_outputs:
            verify_cog_crs(file, expected_results["expected_crs"])
            with rasterio.open(file) as src:
                src.read(1)  # Read the first band

                assert (
                    src.bounds in expected_results["expected_bounding_box"]
                ), f"Bounds didn't match: Expected {expected_results['expected_bounding_box']}, got {src.bounds}"
                print_success(f"Correct Bounding Box: {src.bounds}")

        # Use md5sums to compare previously returned outputs
        actual_md5sums = {
            # file extension: md5sum
            f"science{file.name.split('science')[1]}": hashlib.md5(
                file.read_bytes()
            ).hexdigest()
            for file in downloaded_cog_outputs
        }

    md5sums_path = Path("md5sums") / f"{test_case}.json"
    if save_md5sums:
        print(f"Saving md5sums to {md5sums_path}")
        md5sums_path.write_text(json.dumps(actual_md5sums, indent=4) + "\n")
    else:
        print(f"Verifying existing md5sums for test case {test_case}")
        expected_md5sums = json.load(md5sums_path.open())
        assert (
            actual_md5sums == expected_md5sums
        ), f"md5sums for {test_case} do not match expected"


def assert_dataset_produced_correct_results(
    generated_file: Path, reference_file: Path
) -> None:
    """Check that the generated data matches the expected data."""
    with (
        rasterio.open(generated_file) as test_dataset,
        rasterio.open(reference_file) as reference_dataset,
    ):
        assert (
            test_dataset.meta == reference_dataset.meta
        ), f"output has incorrect metadata: {test_dataset.meta}"
        print_success("Generated image has correct metadata.")

        ref_image = reference_dataset.read()
        test_image = test_dataset.read()
        assert_array_almost_equal(ref_image, test_image)

    print_success("Generated image contains correct data.")


def validate_bounding_box(cog_file: str, expected_results: dict[str, Any]) -> None:
    """Helper function to open, validate the bounding box, and plot the COG file.

    Checks:

    * The bounding box value in the output file is identical to the expected bounding box

    """
    with rasterio.open(cog_file) as src:
        expected_bboxs = expected_results["expected_bounding_box"]
        assert (
            src.bounds in expected_bboxs
        ), f"Bounds did not match: Expected {expected_bboxs}, got {src.bounds}"
        print_success(f"Correct Bounding Box: {src.bounds}")
