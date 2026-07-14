"""One-off script to generate reference hash files for podaac-l2-subsetter tests.

Run from inside test/podaac-l2-subsetter/:
    conda activate papermill-podaac-l2-subsetter
    python generate_references.py

Requires a .netrc file in the test/ directory with EDL credentials.
"""

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from earthdata_hashdiff import create_nc4_hash_file
from harmony import BBox, Client, Collection, Environment, Request

sys.path.append('../shared_utils')
from utilities import submit_and_download

harmony_client = Client(env=Environment.UAT)

# TODO: Replace with actual collection concept ID and granule name
collection = Collection(id='C1234724470-POCLOUD')
granule = '20250717011501-JPL-L2P_GHRSST-SSTskin-MODIS_A-D-v02.0-fv01.0'
spatial = BBox(-160, 30, -120, 60)
variables = ['l2p_flags', 'sea_surface_temperature']

tests = [
    ('bbox_subset', Request(collection=collection, granule_name=granule, spatial=spatial)),
    ('var_subset', Request(collection=collection, granule_name=granule, variables=variables)),
    (
        'bbox_var_subset',
        Request(
            collection=collection,
            granule_name=granule,
            spatial=spatial,
            variables=variables,
        ),
    ),
    ('passthrough', Request(collection=collection, granule_name=granule)),
]

Path('reference_files').mkdir(exist_ok=True)

for name, request in tests:
    with TemporaryDirectory() as tmp_dir:
        output_path = Path(tmp_dir) / f'{name}.nc4'
        submit_and_download(harmony_client, request, output_path)
        reference_path = f'reference_files/{name}.json'
        create_nc4_hash_file(str(output_path), reference_path)
        print(f'Created {reference_path}')

print('\nDone! Reference files generated. You can now delete this script.')
