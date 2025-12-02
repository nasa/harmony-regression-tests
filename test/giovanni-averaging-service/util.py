"Utility functions for comparing csv and geotiff data produced by a harmony request to their reference files"

import rasterio
import numpy as np
import pandas as pd
import pandas.testing as pdt
from typing import List, Tuple
from io import StringIO


def split_csv_header_and_data(csv_rows: List[str]) -> Tuple[List[str], List[str]]:
    """This is a helper function which splits an area averaged time series CSV into its data header and the data itself"""
    for i, row in enumerate(csv_rows):
        if row.strip() == ",":
            csv_header = csv_rows[: i + 1]
            csv_data = csv_rows[i + 1 :]
            return csv_header, csv_data
    raise ValueError(
        "CSV does not contain a heading separator line with only ',' so the data cannot be compared"
    )


def assert_csv_equal(new_file_path: str, reference_file_path: str):
    """This function checks that the data header and data itself for an area averaged time series CSV matches a reference CSV"""
    with open(new_file_path, "r") as new_file:
        new_file_lines = new_file.readlines()
    with open(reference_file_path, "r") as reference_file:
        reference_file_lines = reference_file.readlines()

    new_file_header, new_file_data = split_csv_header_and_data(new_file_lines)
    reference_file_header, reference_file_data = split_csv_header_and_data(
        reference_file_lines
    )

    assert (
        new_file_header == reference_file_header
    ), "The CSV data header does not match the header in the reference CSV data file"

    new_file_df = pd.read_csv(StringIO("".join(new_file_data)))
    reference_file_df = pd.read_csv(StringIO("".join(reference_file_data)))

    for col in new_file_df.columns:
        pdt.assert_series_equal(
            new_file_df[col],
            reference_file_df[col],
            check_dtype=False,
            rtol=1e-05,
            atol=1e-08,
            check_names=True,
            check_index=False,
            obj=f"Column {col}",
        )


def assert_geotiff_equal(new_file_path: str, reference_file_path: str):
    """This function checks that the relevant metadata and data array for a time averaged map geotiff matches a reference geotiff"""
    with rasterio.open(new_file_path) as new_file, rasterio.open(
        reference_file_path
    ) as reference_file:
        # Compare metadata
        assert (
            new_file.crs == reference_file.crs
        ), "Coordinate reference system differs from reference file"
        assert (
            new_file.transform == reference_file.transform
        ), "Transform differs from reference file"
        assert (
            new_file.count == reference_file.count
        ), "Count differs from reference file"
        assert (
            new_file.width == reference_file.width
        ), "Width differs from reference file"
        assert (
            new_file.height == reference_file.height
        ), "Height differs from reference file"

        # Compare array values
        for i in range(1, new_file.count + 1):
            new_array = new_file.read(i)
            reference_array = reference_file.read(i)
            assert np.allclose(
                new_array, reference_array, rtol=1e-05, atol=1e-08, equal_nan=True
            ), f"Band {i} differs from reference file more than allowed tolerance"
