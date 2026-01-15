# HOSS Reference Files

When generating JSON reference hash files for this test suite, the `skipped_metadata_attributes`
argument should be used as shown below with the attributes specified:
```
from earthdata_hashdiff import create_nc4_hash_file


create_nc4_hash_file(
    '/path/to/netCDF4/or/HDF5/file.nc4',
    '/path/to/JSON/output/location.json',
    skipped_metadata_attributes = {
        'references',
        'build_dmrpp_metadata.created',
        'build_dmrpp_metadata.build_dmrpp',
        'build_dmrpp_metadata.bes',
        'build_dmrpp_metadata.libdap',
        'build_dmrpp_metadata.invocation',
        'build_dmrpp_metadata.configuration',
    }
)
```
The same convention applies when using `create_h5_hash_file` to generate JSON reference hash files.
