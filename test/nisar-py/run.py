import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import harmony

# TODO: parameterize via papermill?
#
# Enable this option if you want to save the md5sums for each test case
# rather than verify them. This is useful for adding new test cases
# or updating existing ones.
save_md5sums = False

harmony_host_url = "https://harmony.uat.earthdata.nasa.gov"

environments = {
    "http://localhost:3000": harmony.Environment.LOCAL,
    "https://harmony.sit.earthdata.nasa.gov": harmony.Environment.SIT,
    "https://harmony.uat.earthdata.nasa.gov": harmony.Environment.UAT,
    "https://harmony.earthdata.nasa.gov": harmony.Environment.PROD,
}
assert harmony_host_url in environments

harmony_client = harmony.Client(env=environments[harmony_host_url])

test_cases = [
    {
        # TODO: still needed?
        # original test case
        "granule_name": "NISAR_L2_PR_GCOV_015_156_A_010_2005_DVDV_A_20230619T000803_20230619T000818_T05000_N_P_J_001",
        "format": "image/png",
    },
    {
        # 20m north polar QP granule in png output (interior Alaska)
        "granule_name": "NISAR_L2_PR_GCOV_008_145_D_054_2005_QPDH_A_20251226T061551_20251226T061609_X05010_N_P_J_001",
        "format": "image/png",
    },
    {
        # 10m utm DH granule in png output (coast of Yemen)
        "granule_name": "NISAR_L2_PR_GCOV_010_136_D_082_4005_DHDH_A_20260118T153232_20260118T153308_X05010_N_F_J_001",
        "format": "image/png",
    },
    {
        # 80m frequencyB DV granule in png output (gulf of mexico)
        "granule_name": "NISAR_L2_PR_GCOV_010_156_D_078_0005_NADV_A_20260120T004801_20260120T004836_X05010_N_F_J_001",
        "format": "image/png",
    },
    {
        # 40m DH granule In geotiff output (new zealand)
        "granule_name": "NISAR_L2_PR_GCOV_004_051_A_155_2005_DHDH_A_20251101T184355_20251101T184430_X05009_N_F_J_001",
        "format": "image/tiff",
    },
    # 20m north polar SH (should fail because it’s single-pol)
    # TODO: test the failure
    # "NISAR_L2_PR_GCOV_010_112_A_045_7700_SHNA_A_20260116T231413_20260116T231433_X05010_N_P_J_001",
]
for test_case in test_cases:
    request = harmony.Request(
        collection=harmony.Collection(id="C1273831195-ASF"),
        labels=["nisar-py-rtests"],
        **test_case,
    )
    job_id = harmony_client.submit(request)
    harmony_client.wait_for_processing(job_id)

    with TemporaryDirectory() as temp_dir:
        urls = list(harmony_client.result_urls(job_id))
        assert len([url for url in urls if url.endswith(".txt")]) == 1

        output_files = [
            Path(harmony_client.download(url, temp_dir).result())
            for url in urls
            if not url.endswith(".txt")
        ]
        actual_md5sums = {
            file.name.split(".", maxsplit=1)[1]: hashlib.md5(
                file.read_bytes()
            ).hexdigest()
            for file in output_files
        }

    md5sums_path = Path("md5sums") / f"{test_case['granule_name']}.json"
    if save_md5sums:
        print(f"Saving md5sums to {md5sums_path}")
        json.dump(actual_md5sums, md5sums_path.open("w"), indent=4)
    else:
        print(f"Verifying existing md5sums for {test_case['granule_name']}")
        expected_md5sums = json.load(md5sums_path.open())
        # TODO: display diff on failure
        assert actual_md5sums == expected_md5sums
