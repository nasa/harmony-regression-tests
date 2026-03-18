import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import harmony

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

    # TODO: add an option for saving the md5sums?

    # with open("expected_md5sums.json") as f:
    #     expected_md5sums = json.load(f)

    md5sums = {}

    with TemporaryDirectory() as temp_dir:
        urls = list(harmony_client.result_urls(job_id))

        # Verify that there are the expected number of files for each filetype.
        # assert len(urls) == 109
        # assert len([url for url in urls if url.endswith(".txt")]) == 1
        # assert len([url for url in urls if url.endswith(".png")]) == 36
        # assert len([url for url in urls if url.endswith(".pgw")]) == 36
        # assert len([url for url in urls if url.endswith(".png.aux.xml")]) == 36

        # Verify that the output file checksums match the expected checksums.
        output_files = [
            Path(harmony_client.download(url, temp_dir).result())
            for url in urls
            if not url.endswith(".txt")
        ]
        for file in output_files:
            key = file.name.split(".", maxsplit=1)[1]
            md5sum = hashlib.md5(file.read_bytes()).hexdigest()
            md5sums[key] = md5sum

    with open(f"md5sums/{granule}.json", "w") as f:
        json.dump(md5sums, f, indent=4)
