"""Simple utility functions used in the regridder test notebook."""
from pathlib import Path
import rasterio
from numpy.testing import assert_array_almost_equal


def print_error(error_string: str) -> str:
    """Print an error, with formatting for red text."""
    print(f'\033[91m{error_string}\033[0m')


def print_success(success_string: str) -> str:
    """Print a success message, with formatting for green text."""
    print(f'\033[92mSuccess: {success_string}\033[0m')

def assert_dataset_produced_correct_results(
    generated_file: Path, expected_metadata: dict, reference_file: Path, file_type: str
) -> None:
    """Check that the generated data matches the expected data."""
    with rasterio.open(generated_file) as test_dataset:
        assert (
            test_dataset.meta == expected_metadata
        ), f'output {file_type} has incorrect metadata: {test_dataset.meta}'
        print_success('Generated image has correct metadata.')

        with rasterio.open(reference_file) as reference_dataset:
            ref_image = reference_dataset.read()
            test_image = test_dataset.read()
            assert_array_almost_equal(ref_image, test_image)

    print_success('Generated image contains correct data.')

def build_file_list(basename: str, path: Path, file_type: str) -> list[Path]:
    if file_type == 'PNG':
        exts = ['.png', '.pgw', '.png.aux.xml']
    else:
        exts = ['.jpg', '.jgw', '.jpg.aux.xml']

    return [Path(str(path / basename) + ext) for ext in exts]
