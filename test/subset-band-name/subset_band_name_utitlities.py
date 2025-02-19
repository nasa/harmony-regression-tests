""""
Utility functions used by the subset-band-name regression tests.
"""

import os
from pyhdf.SD import SD, SDC
from pyhdf.HDF import HDF
from pyhdf.VS import VS
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


def get_all_sds_names(file: str):
    """Get all SDS names from HDF-4 file"""
    file_sd = SD(file, SDC.READ)
    datasets = file_sd.datasets()
    file_sd.end()

    return datasets.keys()


def get_vdata(file: str, vdata_name: str):
    """Retrieve VData frm HDF-4 file"""
    file_hdf = HDF(file)
    file_vs = VS(file_hdf)
    vd = file_vs.attach(vdata_name)
    vdata = vd[:]
    vd.detach()
    file_vs.end()
    file_hdf.close()

    return vdata


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

    # Compare one variable at a time
    if sds_name is not None:
        reference_data = get_sds_data(reference_file, sds_name)
        test_data = get_sds_data(test_file, sds_name)

        return numpy.array_equal(reference_data, test_data)

    # Compare all variables and select VData in files
    else:
        reference_sds_names = get_all_sds_names(reference_file)

        for sds_name in reference_sds_names:
            reference_data = get_sds_data(reference_file, sds_name)
            test_data = get_sds_data(test_file, sds_name)

            if not numpy.array_equal(reference_data, test_data):
                return False

        vdata_names = ['Band_250M', 'Band_500M']

        for name in vdata_names:
            reference_vdata = get_vdata(reference_file, name)
            test_vdata = get_vdata(test_file, name)

            if not numpy.array_equal(reference_vdata, test_vdata):
                return False

        return True
