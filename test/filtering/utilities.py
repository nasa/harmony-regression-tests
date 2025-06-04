import json
import numpy as np
import xarray as xr
from pathlib import Path
from tempfile import TemporaryDirectory
from harmony import Client


def print_success(msg: str) -> None:
    print(f'\033[92mSuccess: {msg}\033[0m')


def print_error(msg: str) -> None:
    print(f'\033[91mError: {msg}\033[0m')


def validate_filter_outputs(harmony_client: Client, harmony_job_id: str) -> None:
    """
    Download the one output file, look up its truth entry in filter_truth.json
    (which now carries "group/variable"), open that group, confirm the var exists,
    count non‐NaNs, and assert it matches the expected count.
    """
    # 1) load the truth table
    truth_path = Path(__file__).parent / "reference_data" / "filter_truth.json"
    with open(truth_path, 'r') as f:
        truth = json.load(f)

    # 2) download
    with TemporaryDirectory() as tmp_dir:
        outs = [
            future.result()
            for future in harmony_client.download_all(
                harmony_job_id, overwrite=True, directory=tmp_dir
            )
        ]
        assert len(outs) == 1, f"Expected 1 output file, got {len(outs)}"
        out_path = Path(outs[0])
        fname = out_path.name
        print_success(f"Got one filtered output file: {fname}")

        # strip numeric prefix
        suffix = fname.split('_', 1)[1]
        assert suffix in truth, f"No truth entry for '{suffix}'"
        entry = truth[suffix]

        # 3) parse "group/variable"
        group_var = entry["variable"]
        if "/" in group_var:
            group, var = group_var.split("/", 1)
        else:
            group = None
            var = group_var
        print_success(f"Expecting variable '{var}' in group '{group or '<root>'}'")

        # 4) open dataset (in the right group)
        ds = (
            xr.open_dataset(out_path, group=group)
            if group
            else xr.open_dataset(out_path)
        )
        print_success(
            f"Opened NetCDF file{' and entered group ' + group if group else ''}"
        )

        # 5) confirm the variable exists
        assert var in ds.data_vars, f"Variable '{var}' not found in group '{group}'"
        print_success(f"Found group/variable: {group or '<root>'}/{var}")

        # 6) count non‐NaNs and compare
        data = ds[var].values
        actual_count = int(np.count_nonzero(~np.isnan(data)))
        expected_count = entry["non_nan_count"]
        assert (
            actual_count == expected_count
        ), f"Non-NaN count mismatch for {var}: got {actual_count}, expected {expected_count}"
        print_success(f"Non-NaN pixel count OK ({actual_count} pixels)")

    print_success("All filtering validations passed!")
