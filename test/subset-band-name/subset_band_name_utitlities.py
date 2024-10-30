""""
Utility functions used by the subset-band-name regression tests.
"""

import os
from pyhdf.SD import SD, SDC
import numpy


def get_sds_data(file: str, sds_name: str):
    sds_data = None
    file_sd = SD(file, SDC.READ)
    datasets = file_sd.datasets()

    if datasets.get(sds_name) is not None:
        print('Obtaining', sds_name, 'data from', file)
        dataset = file_sd.select(sds_name)
        sds_data = dataset.get()

    file_sd.end()
    return sds_data


def remove_results_files() -> None:
    """Remove all HDF-4 files downloaded during the Subset-Band-Name
    regression tests.

    """
    directory_files = os.listdir()

    for directory_file in directory_files:
        if directory_file.endswith('.hdf'):
            os.remove(directory_file)


def compare_data(reference_file: str, test_file: str, sds_name: str) -> bool:
    """Compares two data dimension sizes"""
    reference_data = get_sds_data(reference_file, sds_name)
    test_data = get_sds_data(test_file, sds_name)

    return numpy.array_equal(reference_data, test_data)
