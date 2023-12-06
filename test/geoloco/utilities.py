""""
Common utility functions used by the geoloco regression tests.
"""
import os
from pyhdf.SD import SD, SDC

from harmony import Client, Request
from harmony.harmony import ProcessingFailedException


def submit_and_download(harmony_client: Client, request: Request,
                        file_indicator: str) -> str:
    """ Submit a Harmony request via a `harmony-py` client. Wait for the
        Harmony job to finish, then download the results to the specified file
        path.

    """
    downloaded_filenames = []
    output_filename = None

    try:
        job_id = harmony_client.submit(request)

        for filename in [file_future.result()
                         for file_future
                         in harmony_client.download_all(job_id,
                                                        overwrite=True)]:

            print(f'Downloaded: {filename}')
            downloaded_filenames.extend([filename])

        for filename in downloaded_filenames:
            if file_indicator in filename:
                output_filename = filename
                print(f'Saved output to: {output_filename}')


    except ProcessingFailedException as exception:
        print_error('Harmony request failed to complete successfully.')
        raise exception

    return output_filename


def get_dim_sizes(file: str) -> list[int]:
    ydim = None
    xdim = None
    file_SD = SD(file, SDC.READ)
    datasets = file_SD.datasets()
    if len(datasets) > 0:
        dataset_names = datasets.keys()
        for name in dataset_names:
            dataset = file_SD.select(name)
            dims = dataset.dimensions(full=1)
            ydim = list(dims.values())[0][0]
            xdim = list(dims.values())[1][0]

    file_SD.end()
    return [ydim, xdim]


def get_sds_data(file: str):
    sds_data = None
    file_SD = SD(file, SDC.READ)
    datasets = file_SD.datasets()

    if len(datasets) > 0:
        dataset_names = datasets.keys()
        for name in dataset_names:
            if name == 'Cloud_Mask':
                print('Obtaining ', name, ' data')
                dataset = file_SD.select(name)
                sds_data = dataset.get()

    file_SD.end()
    return sds_data


def remove_results_files() -> None:
    """ Remove all HDF-4 files downloaded during the Geoloco
        regression tests.

    """
    directory_files = os.listdir()

    for directory_file in directory_files:
        if directory_file.endswith('.hdf'):
            os.remove(directory_file)


def print_error(error_string: str) -> str:
    """Print an error, with formatting for red text."""
    print(f'\033[91m{error_string}\033[0m')


def print_success(success_string: str) -> str:
    """Print a success message, with formatting for green text."""
    print(f'\033[92mSuccess: {success_string}\033[0m')