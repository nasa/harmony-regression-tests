from os import makedirs
from shutil import rmtree
from typing import Dict

from harmony import Client, Environment, Request
from imghdr import what as what_file_type
from osgeo.gdal import Info as GdalInfo, Open as GdalOpen
from osgeo.osr import SpatialReference
from numpy import array_equal
from numpy.testing import assert_almost_equal
from pyproj import Transformer


def get_test_granule_id(
    environment: Environment, production_granule_id: str, non_prod_granule_id: str
) -> str:
    """Select either the production or non-production granule concept ID
    based on the environment against which the tests are being run.

    """
    if environment == Environment.PROD:
        granule_id = production_granule_id
    else:
        granule_id = non_prod_granule_id

    return granule_id


def make_request_and_download_result(
    harmony_client: Client, request: Request, output_directory: str
):
    """Use the supplied Harmony client (e.g., Prod, UAT, SIT) to make the
    specified request. Wait for the request to complete, and then save the
    output to a user-specified directory.

    """
    try:
        job_id = harmony_client.submit(request)
        harmony_client.wait_for_processing(job_id, show_progress=True)
        makedirs(output_directory, exist_ok=True)

        return [
            result.result()
            for result in harmony_client.download_all(
                job_id, output_directory, overwrite=True
            )
        ]
    except Exception as exception:
        print(f'Could not download granule: {str(exception)}')
        raise exception


def clean_test_artefacts(output_directory: str):
    """Remove test outputs between tests."""
    rmtree(output_directory)


def check_request_output(output_path: str, expected: Dict):
    """Compare Harmony GDAL Adapter request output GeoTIFF to expected results."""
    output = get_geotiff_information(output_path)

    base_error = f'{output_path} has an unexpected'

    assert output['cs'] == expected['cs'], f'{base_error} CS'
    assert output['proj_cs'] == expected['proj_cs'], f'{base_error} Proj CS'
    assert output['proj_epsg'] == expected['proj_epsg'], f'{base_error} Proj EPSG'
    assert output['gcs'] == expected['gcs'], f'{base_error} GCS'
    assert output['gcs_epsg'] == expected['gcs_epsg'], f'{base_error} GCS EPSG'
    assert output['authority'] == expected['authority'], f'{base_error} authority'
    if output['spatial_extent'] is not None:
        assert_almost_equal(
            output['spatial_extent'],
            expected['spatial_extent'],
            decimal=2,
            err_msg=f'{base_error} spatial extent',
        )

    assert output['n_bands'] == expected['n_bands'], f'{base_error} number of bands'
    assert output['variables'] == expected['variables'], f'{base_error} set of variable'
    assert output['height'] == expected['height'], f'{base_error} height'
    assert output['width'] == expected['width'], f'{base_error} width'

    if 'file_type' in expected:
        assert (
            what_file_type(output_path) == expected['file_type']
        ), f'{base_error} file type'

    if 'reference_image' in expected:
        assert compare_to_reference_image(
            output_path, expected['reference_image']
        ), f'{output_path} array values do not match the reference image'

    print_success('All assertions passed')


def get_geotiff_information(file_path: str) -> dict:
    """Read information from a specified GeoTIFF file."""
    dataset = GdalOpen(file_path)
    bands = dataset.RasterCount
    width = dataset.RasterXSize
    height = dataset.RasterYSize

    geo_transform = dataset.GetGeoTransform()
    minx = geo_transform[0]
    miny = (
        geo_transform[3]
        + dataset.RasterXSize * geo_transform[4]
        + dataset.RasterYSize * geo_transform[5]
    )
    maxx = (
        geo_transform[0]
        + dataset.RasterXSize * geo_transform[1]
        + dataset.RasterYSize * geo_transform[2]
    )
    maxy = geo_transform[3]

    proj = SpatialReference(wkt=dataset.GetProjection())
    gcs = proj.GetAttrValue('GEOGCS', 0)
    authority = proj.GetAttrValue('AUTHORITY', 0)

    if proj.IsProjected() == 1 and proj.IsGeographic() == 0:
        cs = 'Projected'
        proj_cs = proj.GetAttrValue('PROJCS', 0)
        proj_epsg = proj.GetAttrValue('AUTHORITY', 1)
        gcs_epsg = proj.GetAttrValue('PROJCS|GEOGCS|AUTHORITY', 1)

        # Transform projected spatial extent to lat/long (WGS84 EPSG:4326)
        transformer = Transformer.from_crs(f'epsg:{proj_epsg}', 'epsg:4326')
        min_extent = transformer.transform(minx, miny)
        max_extent = transformer.transform(maxx, maxy)
        spatial_extent = [
            round(min_extent[0], 2),
            round(max_extent[0], 2),
            round(min_extent[1], 2),
            round(max_extent[1], 2),
        ]
    elif proj.IsProjected() == 0 and proj.IsGeographic() == 1:
        cs = 'Geographic'
        proj_cs = None
        proj_epsg = None
        gcs_epsg = proj.GetAttrValue('AUTHORITY', 1)
        spatial_extent = [
            round(miny, 2),
            round(maxy, 2),
            round(minx, 2),
            round(maxx, 2),
        ]
    else:
        cs = None
        proj_cs = None
        proj_epsg = None
        gcs_epsg = None
        spatial_extent = None

    dataset = None

    gdinfo = GdalInfo(file_path)

    if file_path.endswith(('.tiff', '.tif', '.png')):
        variable_set = {
            gdinfo_line.strip().partition('= ')[2]
            for gdinfo_line in gdinfo.split('\n')
            if 'Description' in gdinfo_line
        }

        if len(variable_set) == 0:
            variable_set = {
                f'{gdinfo_line[:4]}{gdinfo_line[5]}'
                for gdinfo_line in gdinfo.split('\n')
                if 'Block=' in gdinfo_line
            }
    else:
        variable_set = {}

    gdinfo = None

    return {
        'cs': cs,
        'proj_cs': proj_cs,
        'gcs': gcs,
        'authority': authority,
        'proj_epsg': proj_epsg,
        'gcs_epsg': gcs_epsg,
        'spatial_extent': spatial_extent,
        'variables': variable_set,
        'n_bands': bands,
        'height': height,
        'width': width,
    }


def compare_to_reference_image(test_output: str, reference_image: str) -> bool:
    """Compare the array values of the output GeoTIFF to those of a reference
    image.

    """
    output_dataset = GdalOpen(test_output)
    output_raster = output_dataset.ReadAsArray()
    output_dataset = None

    reference_dataset = GdalOpen(reference_image)
    reference_raster = reference_dataset.ReadAsArray()
    reference_dataset = None

    return array_equal(output_raster, reference_raster)


def print_error(error_string: str) -> str:
    """Print an error, with formatting for red text."""
    print(f'\033[91m{error_string}\033[0m')


def print_success(success_string: str) -> str:
    """Print a success message, with formatting for green text."""
    print(f'\033[92mSuccess: {success_string}\033[0m')
