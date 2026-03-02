import json
import hashlib
import pandas as pd
from zipfile import ZipFile


def create_csv_hash_file(input_file_path: str, reference_file_path: str):
    ref_output = []
    with ZipFile(input_file_path, "r") as z:
        csv_list = [fname for fname in z.namelist() if fname.endswith('.csv')]
        for csv_file in csv_list:
            with z.open(csv_file) as ff:
                df = pd.read_csv(ff, dtype=str, keep_default_na=False)
                df = df.sort_index(axis=1)
                b = df.to_csv(index=False, lineterminator="\n").encode("utf-8")
                ref_output.append(hashlib.sha256(b).hexdigest())

    with open(reference_file_path, 'w') as fout:
        json.dump(ref_output, fout, indent=2)
    return reference_file_path


def csv_matches_reference_hash_file(input_file_path: str, reference_file_path: str):
    json_file_path = create_csv_hash_file(
        input_file_path, input_file_path.with_suffix('.json')
    )
    with open(json_file_path) as file1:
        inp = json.load(file1)
    with open(reference_file_path) as file2:
        ref = json.load(file2)

    return set(inp) == set(ref)
