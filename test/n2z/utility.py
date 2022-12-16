"""Simple utility functions used in the NetCDF-to-Zarr test notebook."""


def print_success(success_string: str) -> str:
    """Print a success message, with formatting for green text."""
    print(f'\033[92mSuccess: {success_string}\033[0m')


def assert_result_has_correct_number_of_stores(results: dict,
                                               expected_stores: int) -> None:
    """
    Verify correct number of zarr stores returned.

    Count the number of results items with type "application/x-zazr" and ensure
    that number matches the expected value.
    """
    zarr_stores = [link for
                   link in results.get('links')
                   if link.get('type') == 'application/x-zarr']
    assert len(zarr_stores) == expected_stores, 'Incorrect number of stores found'
