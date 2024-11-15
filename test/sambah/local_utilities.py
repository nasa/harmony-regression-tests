""" A module containing utility functionality used by the Harmony OPeNDAP
    SubSetter regression tests. These functions are kept out of the Jupyter
    notebook to increase the readability of the regression test suite.

"""
from functools import partial
from os import listdir, remove, replace

from harmony import Client, Request
from harmony.harmony import ProcessingFailedException
import xarray as xr


def compare_results_to_reference_file(results_file_name: str) -> None:
    """Use native `xarray` functionality to compare data values and metadata
    attributes of downloaded results to a reference file.
    """
    results_data = xr.open_datatree(results_file_name)
    reference_data = xr.open_datatree(f"reference_files/{results_file_name}")

    # We have to drop 'subset_files', 
    # because the values contain collection_ids, 
    # which will be different for UAT and PROD
    drop_vars_partial = partial(xr.Dataset.drop_vars, errors="ignore")
    results_data = results_data.map_over_datasets(drop_vars_partial, ("subset_files", ))
    reference_data = reference_data.map_over_datasets(drop_vars_partial, ("subset_files", ))
    
    assert results_data.equals(reference_data), (
        'Output and reference files ' 'do not match.'
    )

    reference_data.close()
    results_data.close()


def remove_results_files() -> None:
    """Remove all NetCDF-4 files downloaded during the regression tests."""
    directory_files = listdir()

    for directory_file in directory_files:
        if directory_file.endswith('.nc4') or directory_file.endswith('.nc'):
            remove(directory_file)

