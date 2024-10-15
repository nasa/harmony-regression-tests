""" A module containing utility functionality used by the Trajectory Subsetter
    regression tests. These functions are kept out of the Jupyter notebook to
    increase the readability of the regression test suite.

"""

from os import listdir, remove


def remove_results_files() -> None:
    """Remove all hdf5 files downloaded during the Trajectory Subsetter
    regression tests.

    """
    directory_files = listdir()

    for directory_file in directory_files:
        if directory_file.endswith('.h5'):
            remove(directory_file)
