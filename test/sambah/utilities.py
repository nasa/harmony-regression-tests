""" A module containing utility functionality used by the Harmony OPeNDAP
    SubSetter regression tests. These functions are kept out of the Jupyter
    notebook to increase the readability of the regression test suite.

"""
from os import listdir, remove, replace

from harmony import Client, Request
from harmony.harmony import ProcessingFailedException
import xarray as xr


def compare_results_to_reference_file(results_file_name: str,
                                      group_name='/') -> None:
    """Use native `xarray` functionality to compare data values and metadata
    attributes of downloaded results to a reference file.
    """
    reference_data = xr.open_dataset(f"reference_files/{results_file_name}", group=group_name)
    results_data = xr.open_dataset(results_file_name, group=group_name)

    assert results_data.equals(reference_data), ('Output and reference files '
                                                 'do not match.')

    reference_data.close()
    results_data.close()


def submit_and_download(harmony_client: Client, request: Request,
                        output_file_name: str):
    """Submit a Harmony request via a `harmony-py` client.

    Wait for the Harmony job to finish, then download the results to the specified file path.
    """
    downloaded_filename = None

    try:
        assert request.is_valid()
        job_id = harmony_client.submit(request)

        for filename in [file_future.result()
                         for file_future
                         in harmony_client.download_all(job_id,
                                                        overwrite=True)]:

            print(f'Downloaded: {filename}')
            downloaded_filename = filename

        if downloaded_filename is not None:
            replace(downloaded_filename, output_file_name)
            print(f'Saved output to: {output_file_name}')

    except ProcessingFailedException as exception:
        print('Harmony request failed to complete successfully.')
        raise exception


def remove_results_files() -> None:
    """ Remove all NetCDF-4 files downloaded during the regression tests.

    """
    directory_files = listdir()

    for directory_file in directory_files:
        if directory_file.endswith('.nc4'):
            remove(directory_file)
