""" A module containing common functionality used by multiple regression tests
    regression tests. These functions are kept out of the Jupyter notebook to
    increase the readability of the regression test suite.

"""

from os import listdir, remove, replace

from harmony import Client, Request
from harmony.harmony import ProcessingFailedException

try:
    from xarray.backends.api import open_datatree
except Exception:
    from datatree import open_datatree


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
            replace(downloaded_filename, output_file_name)
            print(f'Saved output to: {output_file_name}')

    except ProcessingFailedException as exception:
        print_error('Harmony request failed to complete successfully.')
        raise exception


def remove_results_files() -> None:
    """Remove all NetCDF-4 files downloaded during the Swath Projector
    regression tests.

    """
    directory_files = listdir()

    for directory_file in directory_files:
        if directory_file.endswith('.h5'):
            remove(directory_file)


def print_error(error_string: str) -> str:
    """Print an error, with formatting for red text."""
    print(f'\033[91m{error_string}\033[0m')


def print_success(success_string: str) -> str:
    """Print a success message, with formatting for green text."""
    print(f'\033[92mSuccess: {success_string}\033[0m')
