import numpy as np
import xarray as xr
from pathlib import Path
from tempfile import TemporaryDirectory
from harmony import Client

def print_success(msg: str) -> None:
    print(f'\033[92mSuccess: {msg}\033[0m')

def print_error(msg: str) -> None:
    print(f'\033[91mError: {msg}\033[0m')


def validate_filter_outputs(
    harmony_client: Client,
    harmony_job_id: str
) -> None:
    """
    Download the one output COG, open its `product` group and
    the golden filtered netCDF from reference_data/product/,
    then:
      - bitwise-compare the NO2 vertical_column_stratosphere array
      - assert the same number of non-NaN pixels
    """
    var = "vertical_column_stratosphere"

    # 1) download and load the filtered array into memory
    with TemporaryDirectory() as tmp_dir:
        outs = [
            f.result()
            for f in harmony_client.download_all(
                harmony_job_id,
                overwrite=True,
                directory=tmp_dir
            )
        ]
        assert len(outs) == 1, f"Expected 1 output file, got {len(outs)}"
        out_path = Path(outs[0])
        print_success("Got one filtered output file.")

        # open the COG's "product" group and pull the array
        ds_out = xr.open_dataset(out_path, group="product")
        assert var in ds_out.data_vars, (
            f"'{var}' not found in output variables: {list(ds_out.data_vars)}"
        )
        arr_out = ds_out[var].values  # read into memory now

    # 2) find and load the reference file
    ref_dir = Path(__file__).parent / "reference_data"
    # match by the _..._filtered.nc suffix
    suffix = out_path.name.split("_", 1)[-1]
    candidates = list(ref_dir.glob(f"*_{suffix}"))
    assert candidates, f"Missing reference file matching '*_{suffix}'"
    ref_path = candidates[0]
    print_success(f"Found reference filtered file: {ref_path.name}")

    ds_ref = xr.open_dataset(ref_path, group="product")
    assert var in ds_ref.data_vars, (
        f"'{var}' not found in reference variables: {list(ds_ref.data_vars)}"
    )
    arr_ref = ds_ref[var].values

    # 3) bitwise (within float tolerance)
    np.testing.assert_allclose(
        arr_out,
        arr_ref,
        rtol=1e-6, atol=0,
        err_msg=f"'{var}' values differ!"
    )
    print_success(f"'{var}' matches between output and reference.")

    # 4) pixel-count sanity
    cnt_out = np.count_nonzero(~np.isnan(arr_out))
    cnt_ref = np.count_nonzero(~np.isnan(arr_ref))
    assert cnt_out == cnt_ref, (
        f"Non-NaN count mismatch: output={cnt_out}, reference={cnt_ref}"
    )
    print_success(
        f"Non-NaN pixel count OK ({cnt_out} pixels) in both output & reference."
    )

    print_success("All filtering validations passed!")
