This directory contains the files that describe mappings between a service name and the regression
tests that should run based on the name.

- `services_tests_config_prod.json` for Production environment
- `services_tests_config_uat.json` for UAT environment

Generally the mapping is:
 - `key`:  A key from the /service-image-tag endpoint.
 - `value`: A comma separated list of names of regression tests that should be run if the key was triggered either by a change to the service docker image or by a user triggering a workflow_dispatch on the GitHub actions page.

There are a few additional keys beyond the keys returned from the Harmony service-image-tags endpoint.

`"all"` is used to trigger every harmony regression test.
`"harmony"` - triggers harmony regression test
`"nsidc-icesat2"`- triggers nsidc-icesat2 regression test
`"sambah"` - triggers samba regression test
`"harmony-regression"` - triggers harmony-regression test

**The important thing to note is that when you are adding a new service to
harmony and adding its regression tests. You must include a mapping for the
service as described by Harmony's /service-image-tag endpoint to the name of
the regression test as described by the directory name in the regression tests.**
