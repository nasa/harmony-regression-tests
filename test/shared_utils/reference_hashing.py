"""A module containing common functionality used by multiple regression tests.

These functions help build reference files that are scaled down from the raw
expected test output. Instead of comparing netCDF4 files, a JSON file is
produced that contains a hash of each group and variable. This hash includes:

* Metadata attributes, excluding those with timestamps that vary based on when
  the tests are executed.
* Dimensions
* (For variables) the values and shape of the data array.

Main functions for external usage:

* `create_xarray_reference_file` - for writing JSON structure of group and
  variable hashes.
* `get_hashes_from_xarray_input` - for iterating through groups and variables
  in a file and generating a hash for each of them. This can be used both to
  generate the reference file and to also convert request output during test
  execution for comparison to that reference file.

"""

import json
from hashlib import sha256
from pathlib import Path

import numpy as np
import xarray as xr

# All decoding is switched off by default to ensure future changes to xarray do
# not affect regression test results.
XARRAY_DECODE_DEFAULTS = {
    'decode_cf': False,
    'decode_coords': False,
    'decode_timedelta': False,
    'decode_times': False,
}


def create_xarray_reference_file(
    input_file_path: str,
    reference_file_path: str,
    skipped_metadata_attributes: set[str] = set(),
    xarray_kwargs: dict = XARRAY_DECODE_DEFAULTS,
):
    """Calculate and output SHA256 hashs for an xarray compatible file.

    Args:
        input_file_path: Input netCDF4 or HDF5 to parse and generate hashes
            for each variable and group.
        reference_file_path: Output path for JSON file containing mapping of
            variables and groups to a SHA256 hash.
        skipped_metadata_attributes: Names of metadata attributes to omit from
            the derivation of the SHA256 has for all group and variable metadata.
            These will be values that are known to vary and are in addition to
            `history` and `history_json`. The main use-case is metadata attributes
            with timestamps dependent on request execution time.
        xarray_kwargs: dict containing arguments used by `xarray` to open the
            input file as a `DataTree` object. Default is to switch off all decoding
            options.

    """
    parsed_hashes = get_hashes_from_xarray_input(
        input_file_path,
        skipped_metadata_attributes=skipped_metadata_attributes,
        xarray_kwargs=xarray_kwargs,
    )
    write_reference_file(reference_file_path, parsed_hashes)


# Aliases for function above:
create_nc4_hash_file = create_xarray_reference_file
create_h5_hash_file = create_xarray_reference_file


def get_hashes_from_xarray_input(
    input_file_path: str,
    skipped_metadata_attributes: set[str] = set(),
    xarray_kwargs: dict = XARRAY_DECODE_DEFAULTS,
) -> dict[str, str]:
    """Open with xarray, generate hashes for all groups and variables.

    Args:
        input_file_path: Input netCDF4 or HDF5 to parse and generate hashes
            for each variable and group.
        skipped_metadata_attributes: Names of metadata attributes to omit from
            the derivation of the SHA256 has for all group and variable metadata.
            These will be values that are known to vary and are in addition to
            `history` and `history_json`. The main use-case is metadata attributes
            with timestamps dependent on request execution time.
        xarray_kwargs: dict containing arguments used by `xarray` to open the
            input file as a `DataTree` object. Default is to switch off all
            decoding options.

    """
    parsed_hashes = {}
    input_groups = xr.open_groups(input_file_path, **xarray_kwargs)

    for dataset_path, dataset in input_groups.items():
        parsed_hashes.update(
            **get_hash_of_xarray_dataset(
                dataset_path,
                dataset,
                skipped_metadata_attributes,
            )
        )

    return parsed_hashes


def write_reference_file(reference_file_path: str, hash_output: dict[str, str]):
    """Write JSON containing SHA256 hashes to an output file."""
    with open(reference_file_path, 'w', encoding='utf-8') as file_handler:
        json.dump(hash_output, file_handler, indent=2)


def get_hash_of_xarray_dataset(
    dataset_path: str,
    dataset: xr.Dataset,
    skipped_metadata_attributes: set[str],
) -> dict[str, str]:
    """Retrieve hashes of Dataset and all variables contained."""
    return {
        dataset_path: get_xarray_object_hash(dataset, skipped_metadata_attributes),
        **{
            get_full_variable_path(dataset_path, variable_path): get_xarray_object_hash(
                variable,
                skipped_metadata_attributes,
            )
            for variable_path, variable in dataset.variables.items()
        },
    }


def get_xarray_object_hash(
    xarray_object: xr.DataArray | xr.Dataset | xr.Variable,
    skipped_metadata_attributes: set[str],
) -> str:
    """Map an xarray.DataArray or xarray.Dataset to a SHA256 hash.

    The hash maps a combination of:

    * The names of dimensions for the variable or group.
    * Metadata attributes, minus things likely to have
      timestamps reflecting when the output was created.
    * For a variable, the array of data (values and shape).

    """
    metadata_bytes = get_metadata_bytes(
        xarray_object.attrs, skipped_metadata_attributes
    )
    dimensions_bytes = get_dimensions_bytes(xarray_object.dims)

    if isinstance(xarray_object, xr.Dataset):
        variable_array_bytes = None
    else:
        variable_array_bytes = get_numpy_array_bytes(xarray_object.data)

    return get_hash_value(
        metadata_bytes,
        dimensions_bytes,
        variable_array_bytes,
    )


def get_full_variable_path(dataset_path: str, variable_path: str) -> str:
    """Combine xarray.Dataset path and xarray.Variable path."""
    return str(Path(dataset_path) / variable_path)


def get_hash_value(
    metadata_bytes: bytes,
    dimension_bytes: bytes,
    variable_array_bytes: bytes | None = None,
):
    """Return a string of a SHA 256 hash of the inputs.

    This function can be used for both groups and
    variables, with the final argument being optional.

    """
    all_bytes = metadata_bytes + dimension_bytes

    if variable_array_bytes is not None:
        all_bytes += variable_array_bytes

    return sha256(all_bytes).hexdigest()


def get_dimensions_bytes(variable_dimensions: tuple[str]) -> bytes:
    """Convert xarray.DataArray.dims to bytes.

    For variables with no dimensions, xarray.DataArray.dims is an
    empty tuple.

    """
    return str(variable_dimensions).encode('utf-8')


def get_numpy_array_bytes(numpy_array: np.ndarray) -> bytes:
    """Convert a numpy array to a byte string.

    The bytes are a combination of:

    * The shape of the array.
    * The values of each element of the array.

    """
    shape_byte_string = str(numpy_array.shape).encode('utf-8')
    array_byte_representation = numpy_array.tobytes()
    return shape_byte_string + array_byte_representation


def get_metadata_bytes(
    variable_metadata: dict,
    skipped_metadata_attributes: set[str],
) -> bytes:
    """Convert xarray.DataArray.attrs to bytes.

    * The attributes are filtered for values that will contain
      datetimes reflecting processing times.
    * The resulting dictionary will be sorted then converted to a string.
    * That string will be encoded as UTF-8 bytes.

    """
    cleaned_metadata = {
        key: serialise_metadata_value(value)
        for key, value in variable_metadata.items()
        if (not is_varying_attribute(key) and key not in skipped_metadata_attributes)
    }

    return json.dumps(dict(sorted(cleaned_metadata.items()))).encode('utf-8')


def is_varying_attribute(attribute_name: str) -> bool:
    """Determine if metadata can't be used for reference comparison.

    Check currently ensures metadata attribute name is not in a set
    of names expected to contain a datetime value that will change
    based on when a file was transformed.

    """
    return attribute_name in {'history', 'history_json'}


def serialise_metadata_value(metadata_value):
    """Convert metadata value to something that can be written as JSON."""
    if isinstance(metadata_value, np.floating):
        cleaned_value = float(metadata_value)
    elif isinstance(metadata_value, np.integer):
        cleaned_value = int(metadata_value)
    elif isinstance(metadata_value, np.ndarray):
        cleaned_value = sha256(get_numpy_array_bytes(metadata_value)).hexdigest()
    else:
        cleaned_value = metadata_value

    return cleaned_value
