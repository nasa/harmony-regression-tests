"""A module containing utility functionality used by the Harmony OPeNDAP
SubSetter regression tests. These functions are kept out of the Jupyter
notebook to increase the readability of the regression test suite.

"""


def test_is_configured(configuration_settings: dict, collection_key: str) -> bool:
    """A helper function to determine if a test should be run given the
    environment information available.

    The specific check is whether the configuration object exists and, if
    so, if the collection that will be used in the test has been saved in
    that configuration object.

    """
    return (
        configuration_settings is not None
        and configuration_settings.get(collection_key) is not None
    )
