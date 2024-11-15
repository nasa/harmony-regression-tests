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

with TemporaryDirectory() as temp_dir:
    output_files = [Path(future.result()) for future in harmony_client.download_all(job_id, directory=temp_dir)]

    assert len(output_files) == 3
    assert output_files[0].suffixes == ['.png']
    assert output_files[1].suffixes == ['.pgw']
    assert output_files[2].suffixes == ['.png', '.aux', '.xml']

    reference_data = Path(__file__).parent / 'reference_data'
    assert output_files[0].read_bytes() == (reference_data / 'rgb.png').read_bytes()
    assert output_files[1].read_bytes() == (reference_data / 'rgb.pgw').read_bytes()
    assert output_files[2].read_bytes() == (reference_data / 'rgb.png.aux.xml').read_bytes()
