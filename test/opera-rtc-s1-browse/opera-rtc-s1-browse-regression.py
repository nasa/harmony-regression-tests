from filecmp import cmp
from pathlib import Path
from tempfile import TemporaryDirectory

import harmony


harmony_client = harmony.Client(env=harmony.Environment.UAT)

request = harmony.Request(
    collection=harmony.Collection(id='OPERA_L2_RTC-S1_V1'),
    granule_name=['OPERA_L2_RTC-S1_T014-029901-IW1_20241001T165524Z_20241001T215545Z_S1A_30_v1.0'],
    format='image/png',
)
job_id = harmony_client.submit(request)
harmony_client.wait_for_processing(job_id)

reference_data = Path(__file__).parent / 'reference_data'
with TemporaryDirectory() as temp_dir:
    output_files = [future.result() for future in harmony_client.download_all(job_id, directory=temp_dir)]

    assert len(output_files) == 3
    assert output_files[0].endswith('.png')
    assert output_files[1].endswith('.pgw')
    assert output_files[2].endswith('.aux.xml')

    assert cmp(output_files[0], reference_data / 'rgb.png', shallow=False)
    assert cmp(output_files[1], reference_data / 'rgb.pgw', shallow=False)
    assert cmp(output_files[2], reference_data / 'rgb.aux.xml', shallow=False)
