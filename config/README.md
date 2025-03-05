This directory has files containing dictionary mappings of labels (keys) to lists of regression tests that run when the label is selected (values)

The two files describe the environments:
- `services_tests_config_prod.json` for Production environment
- `services_tests_config_uat.json` for UAT environment

Generally the mappings are:

 - `key`:  A Harmony service name directly from the Harmony /service-image-tag endpoint.

 - `value`: A comma separated list of regression tests to run.  These tests, will have a direct dependency on the service, either as the regression for the service or as a regression for a service chain that the service is apart of.

There are a few additional keys/values beyond the keys returned from the Harmony service-image-tags endpoint.

`"all"` is used to trigger every harmony regression test.
`"harmony"` - triggers harmony regression test
`"nsidc-icesat2"`- triggers nsidc-icesat2 regression test
`"sambah"` - triggers samba regression test
`"harmony-regression"` - triggers harmony-regression test


**The important thing to note is that when you are adding a new service to
harmony and adding its regression tests. You must include a mapping for the
service as described by Harmony's /service-image-tag endpoint to the name of
the regression test as described by the directory name in the regression tests.**
