import hashlib
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import rasterio
from harmony import Client

sys.path.append("../shared_utils")
from cog_utils import verify_cog_crs
from utilities import print_success


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
            verify_cog_crs(file, expected_results["expected_crs"], False)
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
