# This is directory that contains common utility functions that can be shared across regression tests.

The next steps would be to add the build arg to the docker build command in the Makefiles

```sh
 docker build -t ghcr.io/nasa/regression-tests-nsidc-icesat2:latest -f ./Dockerfile --build-arg notebook=NSIDC-ICESAT2_Regression.ipynb --build-arg sub_dir=nsidc-icesat2 --build-arg shared_utils=true -f Dockerfile .
 ```

# Will also need to descibe how to use the shared_utils and how to ensure your conda environment has all requirements.


# describe how to import these in your tests

```python
## Import shared utility routines:
from pathlib import Path
import sys

shared_utils = Path(__file__).resolve().parent.parent / 'shared_utils'
sys.path.append(str(shared_utils))
from utilities import print_success  # noqa: E402

print_success('whoopie')
```
