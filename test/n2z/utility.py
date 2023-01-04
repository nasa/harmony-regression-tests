"""Simple utility functions used in the NetCDF-to-Zarr test notebook."""

import boto3
from filecmp import dircmp
import os
from typing import List


def print_success(success_string: str) -> str:
    """Print a success message, with formatting for green text."""
    print(f'\033[92mSuccess: {success_string}\033[0m')


def get_zarr_stores(results: dict) -> List[dict]:
    """Return all results items that are type "application/x-zarr"."""
    return [link for
            link in results.get('links')
            if link.get('type') == 'application/x-zarr']


def assert_result_has_correct_number_of_stores(results: dict,
                                               expected_stores: int) -> None:
    """
    Verify correct number of zarr stores returned.

    Count the number of results items that are zarr stores and ensure
    that number matches the expected value.
    """
    zarr_stores = get_zarr_stores(results)
    assert len(zarr_stores) == expected_stores, 'Incorrect number of stores found'


def get_zarr_store_location(results: dict) -> str:
    """Return s3 location of a results dictionary containing a single zarr store."""
    zarr_stores = get_zarr_stores(results)
    assert len(zarr_stores) == 1
    return zarr_stores[0]['href']


def download_zarr_store(zarr_s3_url: str,
                        local_directory: str,
                        endpoint_url: str = None) -> None:
    """Download a zarr store from S3 to the desired location.

    zarr_s3_url - location of the zarr store on s3
    endpoint_url - optional location of the s3 endpoint to use

    """
    s3 = boto3.client('s3', endpoint_url=endpoint_url)

    bucket_name = zarr_s3_url.split('/')[2]
    prefix = '/'.join(zarr_s3_url.split('/')[3:])

    s3_objects = s3.list_objects(Bucket=bucket_name, Prefix=prefix)['Contents']

    zarr_object_names = [o['Key'] for o in s3_objects]
    commonprefix = os.path.commonprefix(zarr_object_names)

    for object_name in zarr_object_names:
        local_filename = object_name.replace(commonprefix, '')
        full_local_filename = os.path.join(local_directory, local_filename)
        if not os.path.exists(os.path.dirname(full_local_filename)):
            os.makedirs(os.path.dirname(full_local_filename))
        s3.download_file(bucket_name, object_name, full_local_filename)


def assert_zarr_store_matches_reference_data(
        download_store: str,
        reference_store: str,
) -> None:
    """Compare downloaded store to reference store."""
    comparison = dircmp(download_store, reference_store)
    if len(comparison.diff_files) == 0:
        print_success('Zarr store matches reference')
    else:
        print(f'Bad files: {comparison.diff_files}')
        raise Exception('Zarr store does not match reference store')
