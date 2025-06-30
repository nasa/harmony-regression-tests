import filecmp
from pathlib import Path
from tempfile import TemporaryDirectory
from harmony import Client

def print_success(msg: str) -> None:
    print(f'\033[92mSuccess: {msg}\033[0m')

def print_error(msg: str) -> None:
    print(f'\033[91mError: {msg}\033[0m')

def validate_imagenator_outputs(
    harmony_client: Client,
    harmony_job_id: str
) -> None:
    """
    Download all outputs for an Imagenator job (3 files: .paw, .png, .xml-aux, etc).
    Ignore any leading "<digits>_" prefix on the filename when matching
    to reference_data/<core_name>.
    """
    ref_dir = Path(__file__).parent / "reference_data"

    # Keep the temp dir alive through download AND comparison
    with TemporaryDirectory() as tmp_dir:
        # 1) Download all outputs
        futures = list(harmony_client.download_all(
            harmony_job_id,
            overwrite=True,
            directory=tmp_dir
        ))
        print(f"DEBUG: download_all returned {len(futures)} future(s)")
        outs = [f.result() for f in futures]
        print(f"DEBUG: downloaded files: {outs}")

        # 2) Sanity: expect 3 files
        expected_count = 3
        if len(outs) != expected_count:
            raise AssertionError(
                f"Expected {expected_count} output files, got {len(outs)}: {outs}"
            )
        print_success(f"Downloaded {len(outs)} output files.")

        # 3) For each downloaded file:
        for out_path_str in outs:
            out_path = Path(out_path_str)
            fname = out_path.name

            # strip leading digits: "12345_TEMPO_..." → "TEMPO_..."
            if "_" in fname and fname.split("_",1)[0].isdigit():
                core = fname.split("_", 1)[1]
            else:
                core = fname

            # log level detection (optional)
            level = "L2" if "_L2_" in core else "L3" if "_L3_" in core else "unknown"
            print(f"Validating {fname} → {core} (level={level})...")

            # 4) find the reference file
            ref_path = ref_dir / core
            if not ref_path.exists():
                raise AssertionError(f"Missing reference file: {ref_path}")

            # 5) byte-for-byte comparison
            if not filecmp.cmp(out_path, ref_path, shallow=False):
                raise AssertionError(f"Contents differ for {core}")

            print_success(f"{core} matches reference.")

        # exiting with-block will now clean up tmp_dir
    print_success("All IMAGENATOR outputs match their reference files!")
