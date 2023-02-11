import cdk_root_pipeline.utils as utils


def test_get_resource_name_happy_full():
    resource_name = utils.get_resource_name(
        environment='dev',
        resource_name='dataprocessing',
        resource_type='fn',
        component_name='transformer'
    )
    print(resource_name)
    assert resource_name == 'dev-transformer-dataprocessing-fn-thy'


def test_get_resource_name_happy_root_setup():
    resource_name = utils.get_resource_name(
        resource_name='rootbootstrap',
        resource_type='repo',
    )
    print(resource_name)
    assert resource_name == 'rootbootstrap-repo-thy'


def test_get_resource_name_unhappy():
    pass
