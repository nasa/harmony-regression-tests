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
    subset_selector: dict | None = None,
) -> None:
    """Compare two files as DataTrees

    Args:
        results_file_name: Path to the results file to validate

        reference_file_name: Path to the reference file to compare against

        identical: If True, use strict comparison including attributes; if
                   False, compare only values

        coordinates_to_fix: List of coordinate names to be renamed in the case
                            that the input has "unalignable" names.

        subset_selector: Dict of top level group names to selection
                         dictionaries used to subset the input DataTree to the
                         previously subsetted reference data. (see
                         `subset_datatree`'s doc string for more information)

    Raises:
      AssertionError: when files don't match according to comparison criteria.

    """
    if coordinates_to_fix is None:
        coordinates_to_fix = []

    reference_groups = open_groups(reference_file_name, decode_times=False)
    results_groups = open_groups(results_file_name, decode_times=False)

    # Fix unalignable coordinates
    for coord in coordinates_to_fix:
        reference_groups = unalign_groups(reference_groups, coord)
        results_groups = unalign_groups(results_groups, coord)

    reference_data = DataTree.from_dict(reference_groups)
    results_data = DataTree.from_dict(results_groups)

    # Limit comparison of data
    if subset_selector is not None:
        results_data = subset_datatree(results_data, subset_selector)

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


def subset_datatree(dt: DataTree, selectors: dict[str, dict]) -> DataTree:
    """Using a selector dictionary return a subset of the input DataTree.

    Args:
        dt: Input Datatree to subset
        selectors: Dictionary mapping top level group names to dictionaries,
                   where each dictionary contains dimension names to indices
                   selected by slice.

    a sample selector dictionary:
    selectors = {
        "Soil_Moisture_Retrieval_Data_3km": {
            "y-dim": slice(1000, 2000),
            "x-dim": slice(8800, 9800),
        },
        "Soil_Moisture_Retrieval_Data": {
            "y-dim": slice(0, 1000),
            "x-dim": slice(2500, 3500),
        },
    }

    This is used to subset the SPL2SMAP granule, the data groups are the keys
    and the dimensions are subset into 1000x1000 grids that include valid
    output data.
    """
    out_dt = dt.copy()
    for group_name, slices in selectors.items():
        out_dt[group_name] = out_dt[group_name].isel(slices)
    return out_dt


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
