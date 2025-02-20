"""A module containing utility functionality used by the Variable Subsetter
regression tests. These functions are kept out of the Jupyter notebook to
increase the readability of the regression test suite.

"""

from os import listdir, remove, replace
from typing import Union

from harmony import Client, Request
from harmony.harmony import ProcessingFailedException
from netCDF4 import Dataset, Group, Variable
import numpy as np


GroupOrVariable = Union[Group, Variable]


def compare_attributes_to_reference(
    results_object: GroupOrVariable, ref_object: GroupOrVariable
):
    """Ensure the metadata attributes of two NetCDF-4 objects (groups or
    variables) are the same, with the exception of `history` and
    `history_json`, which will include references to the request time.

    """
    assert results_object.ncattrs() == ref_object.ncattrs()

    for attribute_name, ref_attribute_value in ref_object.__dict__.items():
        if attribute_name not in ['history', 'history_json']:
            if isinstance(ref_attribute_value, np.ndarray):
                np.testing.assert_array_equal(
                    results_object.getncattr(attribute_name), ref_attribute_value
                )
            else:
                assert results_object.getncattr(attribute_name) == ref_attribute_value


def compare_variable_to_reference(results_variable: Variable, ref_variable: Variable):
    """Compare two NetCDF-4 variables, ensuring they have the same data in
    their arrays and the same metadata attribute.

    """
    np.testing.assert_array_equal(results_variable[:], ref_variable[:])
    compare_attributes_to_reference(results_variable, ref_variable)


def compare_group_to_reference(results_group: Group, ref_group: Group):
    """Compare two NetCDF-4 file groups, ensuring they have the same metadata
    attributes (excluding provenance), child variables and child groups.
    Child variables and groups are then compared recursively.

    """
    compare_attributes_to_reference(results_group, ref_group)

    assert list(results_group.groups.keys()) == list(ref_group.groups.keys())
    assert list(results_group.variables.keys()) == list(ref_group.variables.keys())

    for variable_name, ref_variable in ref_group.variables.items():
        compare_variable_to_reference(results_group[variable_name], ref_variable)

    for child_group_name, ref_child_group in ref_group.groups.items():
        compare_group_to_reference(results_group[child_group_name], ref_child_group)


def compare_results_to_reference_file(results_file: str, ref_file: str):
    """Compare two NetCDF-4 files recursively, checking that the both have the
    same group structure, variables and metadata attributes.

    """
    with Dataset(results_file) as results_ds, Dataset(ref_file) as ref_ds:
        compare_group_to_reference(results_ds, ref_ds)


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
        if directory_file.endswith('.nc4'):
            remove(directory_file)


def print_error(error_string: str) -> str:
    """Print an error, with formatting for red text."""
    print(f'\033[91m{error_string}\033[0m')


def print_success(success_string: str) -> str:
    """Print a success message, with formatting for green text."""
    print(f'\033[92mSuccess: {success_string}\033[0m')
