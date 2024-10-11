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
) -> None:
    """Use `DataTree` functionality to compare data values, variables,
    coordinates, metadata, and all their corresponding attributes of
    downloaded results to a reference file.

    """
    if coordinates_to_fix is None:
        coordinates_to_fix = []

    reference_groups = open_groups(reference_file_name)
    results_groups = open_groups(results_file_name)

    # Fix unalignable coordinates
    for coord in coordinates_to_fix:
        reference_groups = unalign_groups(reference_groups, coord)
        results_groups = unalign_groups(results_groups, coord)

    reference_data = DataTree.from_dict(reference_groups)
    results_data = DataTree.from_dict(results_groups)

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
