""""
Utility functions used by the subset-band-name regression tests.
"""

import os
from pyhdf.SD import SD, SDC
import numpy


def get_sds_data(file: str):
    sds_data = None
    file_SD = SD(file, SDC.READ)
    datasets = file_SD.datasets()

    for key in datasets.keys():
        if key == 'EV_250_Aggr500_RefSB':
            print('Obtaining ', key, ' data')
            dataset = file_SD.select(key)
            sds_data = dataset.get()

    file_SD.end()
    return sds_data


def remove_results_files() -> None:
    """Remove all HDF-4 files downloaded during the Subset-Band-Name
    regression tests.

    """
    directory_files = os.listdir()

    for directory_file in directory_files:
        if directory_file.endswith('.hdf'):
            os.remove(directory_file)


def compare_data(reference_file: str, test_file: str) -> bool:
    """Compares two data dimension sizes"""
    reference_data = get_sds_data(reference_file)
    test_data = get_sds_data(test_file)

    return numpy.array_equal(reference_data, test_data)
