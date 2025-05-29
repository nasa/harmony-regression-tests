# CHANGELOG

The harmony-regression-tests repository does not follow semantic
versioning. Rather than a static releases, this repository contains of a number
of regression tests that are each semi-independent.  This CHANGELOG file should be used
to document pull requests to this repository.

## 2025-05-29 ([#172](https://github.com/nasa/harmony-regression-tests/pull/172))

### Added

- Adds regression tests for asdc/filtering service chain.

## 2025-05-22 ([#169](https://github.com/nasa/harmony-regression-tests/pull/169))

### Changed

- net2cog, HyBIG and opera-rtc-s1-browse reference images have been migrated
  out of `git-lfs` and the CI/CD for building those Docker images has been
  update to not use `git-lfs`.

## 2025-05-12 ([#167](https://github.com/nasa/harmony-regression-tests/pull/167))

### Changed

- ATL16 regridding service reference file updated to reflect corrected missing data handling.


## 2025-05-02 [#165](https://github.com/nasa/harmony-regression-tests/pull/165))

### Changed

- ATL08_subset_by_temporal_range_reference.h5
- NSIDC-ICESAT2_Regression.ipynb, updated with correct granule IDs and temporal test for ATL08

## 2025-04-15 ([#161](https://github.com/nasa/harmony-regression-tests/pull/161))

### Removed

- NetCDF-to-Zarr regression test suite, due to pending service deprecation.
- AWS credentials within Docker images, as they were only used by NetCDF-to-Zarr.
- NetCDF-to-Zarr service invocation in `HarmonyRegression.ipynb`.

### Changed

- Pinned `harmony-py` dependency for Swath Projector and Variable Subsetter test
  suites. Updated utility functions for each to use updated import paths for
  `ProcessingFailedException`.

## 2025-04-09 ([#159](https://github.com/nasa/harmony-regression-tests/pull/159))

- Update reference files in SAMBAH test case to reflect updates to Harmony UAT processing.

## 2025-03-21 ([#156](https://github.com/nasa/harmony-regression-tests/pull/156))

- Update the NSIDC regression test notebook to incorporate the ATL08 test and
  associated reference file now that the bug that affected temporal subsetting
  for segmented collections has been resolved.

## 2025-03-20 ([#155](https://github.com/nasa/harmony-regression-tests/pull/155))

- Update and rename reference files in HOSS test cases to reflect SMAP L3
  maskfill spatial subsetting changes.

## 2025-03-19 ([#151](https://github.com/nasa/harmony-regression-tests/pull/151))

- Upgrade regridder regression tests. Upgrade python libraies. Use shared
  utilities.

## 2025-03-13 ([#153](https://github.com/nasa/harmony-regression-tests/pull/153))

- Fix a bug in subset-band-name band subsetting test case where file
  comparisons were being run when Production testing is disabled.

## 2025-03-12 ([#152](https://github.com/nasa/harmony-regression-tests/pull/152))

- Add SPL3SMP_E, SPL3SMP, and SPL3FTP_E tests to HOSS_Regression.ipynb.

## 2025-03-06 ([#148](https://github.com/nasa/harmony-regression-tests/pull/148))

- Fix service name key missed in [#147](https://github.com/nasa/harmony-regression-tests/pull/147).

## 2025-03-05 ([#147](https://github.com/nasa/harmony-regression-tests/pull/147))

- Clean up `repository_dispatch` and `workflow_dispatch` options to be
  consistent with Harmony's service-image-tags endpoint.
- Adds documentation to clarify how the configuration works for mapping
  triggers to regression tests.

## 2025-03-04 ([#146](https://github.com/nasa/harmony-regression-tests/pull/146))

- Re-enable two ATL10 v006 tests in the nsidc-icesat2 regression notebook, as
  the Trajectory Subsetter now supports ATL10 v006.

## 2025-03-03 ([#145](https://github.com/nasa/harmony-regression-tests/pull/145))

- Fix mismatched service to regression links in config and test workflows.

## 2025-02-28 ([#143](https://github.com/nasa/harmony-regression-tests/pull/143))

- Force sambah image build.

## 2025-02-28 ([#142](https://github.com/nasa/harmony-regression-tests/pull/142))

- Upgrade harmony-py to v1.0.0 for all tests that use the shared utilities.
  These are the nsidc-icesat2, sambah, smap-l2-gridder, subset-band-name and
  trajectory-subsetter tests.
- Bump patch versions of each test.
- Add version.txt to sambah tests.

## 2025-02-28 ([#139](https://github.com/nasa/harmony-regression-tests/pull/139))

- Add missing SAMBAH references to GitHub Actions workflow.

## 2025-02-25 ([#141](https://github.com/nasa/harmony-regression-tests/pull/141))

- Update ATL10 v006 reference files for the NSIDC Trajectory Subsetter
  regression tests.

## 2025-02-19 ([#137](https://github.com/nasa/harmony-regression-tests/pull/137))

- Add configuration for the [SPL2SMP](https://nsidc.org/data/spl2smp/versions/9)
  collection to harmony-smap-l2-gridder.

## 2025-02-12 ([#116](https://github.com/nasa/harmony-regression-tests/pull/116))

- Add tests for SAMBAH service chain.

## 2025-02-12 ([#135](https://github.com/nasa/harmony-regression-tests/pull/135))

- Add band subsetting test case to subset-band-name tests.
- Add Production IDs to geoloco tests.

## 2025-02-05 ([#134](https://github.com/nasa/harmony-regression-tests/pull/134))

- Add configuration for the [SPL2SMA](https://nsidc.org/data/spl2sma/versions/3)
  collection to harmony-smap-l2-gridder.

## 2025-02-04([#131](https://github.com/nasa/harmony-regression-tests/pull/131))

- Update net2cog tests to include single, multiple and all variable test cases.

## 2025-01-31 ([#130](https://github.com/nasa/harmony-regression-tests/pull/130))

- Add tests and configuration for harmony-smap-l2-gridder.

## 2024-12-20([#126](https://github.com/nasa/harmony-regression-tests/pull/126))

- Update configuration to run `opera-rtc-s1-browse` tests on HyBIG deployments.

## 2024-12-19 ([#125](https://github.com/nasa/harmony-regression-tests/pull/125))

- Update HyBIG test images to account for increased color map range (DAS-2280).

## 2024-12-16 ([#122](https://github.com/nasa/harmony-regression-tests/pull/122))([#123](https://github.com/nasa/harmony-regression-tests/pull/123))

- Update HyBIG test images to account for changes in how HyBIG treats 3 and 4
  band input GeoTIFFs.
- Set HyBIG reference images to be tracked by git lfs.
- Update opera-rtc-s1-browse test images to account for changes in HyBIG v2.1.0.

## 2024-11-06 ([#112](https://github.com/nasa/harmony-regression-tests/pull/112))

- Ensure conda packages are installed from conda-forge.

## 2024-10-31 ([#107](https://github.com/nasa/harmony-regression-tests/pull/107))

- Update the net2cog regression test suite to ensure that failures do not
  happen for environments against which the test suite is not configured. Prior
  to this change an undefined variable was causing issues when running the test
  suite against production.

## 2024-10-30 ([#111](https://github.com/nasa/harmony-regression-tests/pull/111))

- Update the swath-projector epsg reference file.

## 2024-10-29 ([#95](https://github.com/nasa/harmony-regression-tests/pull/95))

- Add LAADS DAAC subset-band-name test suite with subsetting EV_250_Aggr500_RefSB
  variable MOD02HKM collection as a starter test.
- Utilize functions from `shared_utils`.

## 2024-10-16 ([#105](https://github.com/nasa/harmony-regression-tests/pull/105))

- Update the HyBIG regression test suite to include a test specifying a variable
  in the request. This will ensure Harmony passes UMM-Var metadata to HyBIG and
  therefore allow HyBIG to use a custom colour map for the generated browse
  imagery.
- The comparisons within the HyBIG regression test suite also now derive their
  CRS and geotransform metadata from the `.aux.xml` file for each browse image.

## 2024-10-11 ([#104](https://github.com/nasa/harmony-regression-tests/pull/104))

- Migrate trajectory-subsetter to use `shared_utils`.
- Separate `shared_utils/utilities.py` into `utilities.py` and `compare.py`
  preventing `xarray` from being a mandatory requirement to use `shared_utils`.
- Update `shared_utils` `README` to mention the github action updates needed
  to use `shared_utils`.
- Remove old `compare_results_to_reference_file` and renames
  `compare_results_to_reference_file_new` -> `compare_results_to_reference_file`.
- Migrate nsidc_icesat2 tests to the new `shared_utils` structure and names.

## 2024-10-11 ([#103](https://github.com/nasa/harmony-regression-tests/pull/103))

- Update the ATL03 and ATL08 reference files in the `nsidc-icesat2` regression
  test notebook to adjust to the DAS-2205 bug fix.
- Update the `shared_utils` function `compare_results_to_reference_file_new`
  to surround comparison assertion with a `try`/`except` so all tests are run
  even when a comparison fails.

## 2024-10-02 ([#99](https://github.com/nasa/harmony-regression-tests/pull/99))

- Add NSIDC ICESat2 Production Regression configuration.
- Update the `shared_utils` function `compare_results_to_reference_file_new`
  to take a new optional argument `identical` which defaults to `True` but if
  set to `False` the Datatree comparison falls back to an `equals` test
  ignoring metadata in its reference file comparisons.


## 2024-09-24 ([#92](https://github.com/nasa/harmony-regression-tests/pull/92))

- Add NSIDC ICESat2 Regression test suite.

- Add `shared_utils` functionality. This directory contains routines that are
  commonly used in regression tests and limits code duplication. To include the
  `shared_utils` directory in your docker container, update the `Makefile` to
  add a shared_utils build arg. E.g. `--build-arg shared_utils=true` and update
  the `.github/workflows/build-all-images.yml` to add a `shared-utils` key of
  "true" (see the nsidc-icesat2-image target in each file).

- Add Git LFS functionality. Large files can be configured to use [Git LFS](https://git-lfs.com/).
  This PR configures the NSIDC reference files `test/nsidc-icesat2/reference_files/*.h5`.


## 2024-08-30 ([#94](https://github.com/nasa/harmony-regression-tests/pull/94))

- Add regression test for net2cog.

## 2024-08-05 ([#86](https://github.com/nasa/harmony-regression-tests/pull/86))

- Add this file to capture changes to the repository.

- Add pre-commit.ci behavior to the repository. This setup ensures consistent
  code style, catches common errors, and maintains file hygiene across the project.

- Update the base image for all regression tests to `mambaorg/micromamba:1.5.8-jammy`.
