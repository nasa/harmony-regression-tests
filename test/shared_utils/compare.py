"""A module containing common functionality used by multiple regression
tests. These functions are kept out of the Jupyter notebook to increase the
readability of the regression test suite.

This module focuses on comparing output specifically with xarray.
"""

from itertools import count


from xarray.backends.api import open_groups
from xarray.core.datatree import DataTree
from xarray import Dataset


def compare_results_to_reference_file(
    results_file_name: str,
    reference_file_name: str,
    identical: bool = True,
    coordinates_to_fix: list[str] | None = None,
    limit_comparison_dimensions: dict | None = None,
) -> None:
    """Compare two files as DataTrees

    Args:
        results_file_name: Path to the results file to validate
        reference_file_name: Path to the reference file to compare against
        identical: If True, use strict comparison including attributes; if False, compare only values
        coordinates_to_fix: List of coordinate names to be renamed in the case that the input has "unalignable" names.
        limit_comparison_dimensions: Dict of dimension names and indices to limit comparison scope

    Raises:
      AssertionError: when files don't match according to comparison criteria.

    """
    if coordinates_to_fix is None:
        coordinates_to_fix = []

    reference_groups = open_groups(reference_file_name, decode_timedelta=False)
    results_groups = open_groups(results_file_name, decode_timedelta=False)

    # Fix unalignable coordinates
    for coord in coordinates_to_fix:
        reference_groups = unalign_groups(reference_groups, coord)
        results_groups = unalign_groups(results_groups, coord)

    reference_data = DataTree.from_dict(reference_groups)
    results_data = DataTree.from_dict(results_groups)

    # Limit comparison of data
    if limit_comparison_dimensions is not None:
        reference_data = reference_data.isel(limit_comparison_dimensions)
        results_data = results_data.isel(limit_comparison_dimensions)

    if identical:
        assert results_data.identical(
            reference_data
        ), 'Output and reference files do not match.'
    else:
        assert results_data.equals(
            reference_data
        ), 'Output and reference files do not match.'

    reference_data = None
    results_data = None


def unalign_groups(
    dict_of_datasets: dict[str, Dataset], coordinate: str
) -> dict[str, Dataset]:
    """Rename coordinates with different dimensions across datasets.

    This function addresses the issue of datasets having coordinates with the
    same name but different dimensions, which causes problems when creating a
    DataTree. Specifically for handling data products like ATL04 ICESat2, where
    common coordinates (e.g., "delta_time") have different lengths across
    datasets.

    The function renames the specified coordinate in each dataset where it appears,
    assigning a unique identifier to each instance. This allows for the creation of
    a DataTree from the modified dictionary of datasets.

    Parameters:
    -----------
    dict_of_datasets : dict[str, Dataset]
        A dictionary of xarray Datasets, typically obtained from xarray.open_groups().
    coordinate : str
        The name of the coordinate to be renamed across Datasets.

    Returns:
    --------
    dict[str, Dataset]
        A new dictionary of datasets with the specified coordinate
        incrementally renamed when present.

    """
    counter = count(1)
    return {
        key: (
            ds.rename({coordinate: f"{coordinate}_{next(counter)}"})
            if coordinate in ds.coords
            else ds
        )
        for key, ds in dict_of_datasets.items()
    }
