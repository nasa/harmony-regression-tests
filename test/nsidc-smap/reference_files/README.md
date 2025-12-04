# NSIDC-SMAP Reference Files

When generating JSON reference hash files for this test suite, the `skipped_metadata_attributes`
argument should be used as shown below with the attributes specified:
```
from earthdata_hashdiff import create_nc4_hash_file

create_nc4_hash_file(
    '/path/to/netCDF4/or/HDF5/file.nc4',
    '/path/to/JSON/output/location.json',
    'skipped_metadata_attributes': {
        'build_dmrpp_metadata.invocation',
        'build_dmrpp_metadata.configuration',
        'Processing Parameters',
    }
)
```
The same convention applies when using `create_h5_hash_file` to generate JSON reference hash files.
