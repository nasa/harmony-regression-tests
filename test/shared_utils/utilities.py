""" A module containing common functionality used by multiple regression tests
    regression tests. These functions are kept out of the Jupyter notebook to
    increase the readability of the regression test suite.

"""

from shutil import move
from itertools import count

from harmony import Client, Request
from harmony.harmony import ProcessingFailedException

try:
    from xarray.backends.api import open_groups
    from xarray.core.datatree import DataTree
    from xarray import Dataset
except Exception:
    # only used by Trajectory Subsetter tests.
    # TODO: remove and make Trajectory Subsetter use above
    from datatree import open_datatree


def print_error(error_string: str) -> str:
    """Print an error, with formatting for red text."""
    print(f'\033[91m{error_string}\033[0m')


def print_success(success_string: str) -> str:
    """Print a success message, with formatting for green text."""
    print(f'\033[92mSuccess: {success_string}\033[0m')


def submit_and_download(
    harmony_client: Client, request: Request, output_file_name: str
):
    """Submit a Harmony request via a `harmony-py` client. Wait for the
    Harmony job to finish, then download the results to the specified file
    path.

    """
    downloaded_filename = None

    try:
        job_id = harmony_client.submit(request)

        for filename in [
            file_future.result()
            for file_future in harmony_client.download_all(job_id, overwrite=True)
        ]:

            print(f'Downloaded: {filename}')
            downloaded_filename = filename

        if downloaded_filename is not None:
            move(downloaded_filename, output_file_name)
            print(f'Saved output to: {output_file_name}')

    except ProcessingFailedException as exception:
        print_error('Harmony request failed to complete successfully.')
        raise exception


def compare_results_to_reference_file(
    results_file_name: str, reference_file_name: str
) -> None:
    """Use `DataTree` functionality to compare data values, variables,
    coordinates, metadata, and all their corresponding attributes of
    downloaded results to a reference file.

    """
    reference_data = open_datatree(reference_file_name)
    results_data = open_datatree(results_file_name)

    assert results_data.identical(reference_data), (
        'Output and reference files ' 'do not match.'
    )

    reference_data = None
    results_data = None


def compare_results_to_reference_file_new(
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
