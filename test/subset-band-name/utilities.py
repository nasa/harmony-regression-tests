""""
Utility functions used by the subset-band-name regression tests.
"""

import os
from pyhdf.SD import SD, SDC
import numpy


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
    if numpy.array_equal(reference_data, test_data):
        return True
    else:
        return False
