# shared utitities for comparing COG outputs

from os.path import basename


from rio_cogeo.cogeo import cog_info, cog_validate
from utilities import print_success


def verify_cog_crs(downloaded_cog_file, expected_crs: str, check_cog: bool):
    """Verify output file is valid COG and CRS is correct"""
    print(f"Assessing: {basename(downloaded_cog_file)}")

    if check_cog:
        assert cog_validate(downloaded_cog_file)[0]
        print_success("Generated output files is a valid COG.")

    assert (
        cog_info(downloaded_cog_file).GEO.CRS == expected_crs
    ), f"Expected crs {expected_crs}, got {cog_info(downloaded_cog_file).GEO.CRS}"

    print_success(
        f"Correct Coordinate Reference System (CRS): {cog_info(downloaded_cog_file).GEO.CRS}"
    )
