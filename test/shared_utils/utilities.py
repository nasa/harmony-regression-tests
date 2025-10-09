"""A module containing common functionality used by multiple
regression tests. These functions are kept out of the Jupyter notebook to
increase the readability of the regression test suite.

"""

from shutil import move
from pathlib import Path

from harmony import Client, Request
from harmony.client import ProcessingFailedException


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


def download_file_from_harmony(
    harmony_client: Client,
    job_id: str,
    target_filename: str | Path,
    working_dir: str | Path = "",
):
    """Download a single file result from Harmony into the target_filename provided."""

    files = [
        file_future.result()
        for file_future in harmony_client.download_all(
            job_id, overwrite=True, directory=str(working_dir)
        )
    ]

    if len(files) > 1:
        print(
            f"Warning: Harmony job generated {len(files)} files. Only first file is saved at {target_filename}."
        )

    Path(files[0]).replace(target_filename)
    print(f"Downloaded to: {target_filename}")
