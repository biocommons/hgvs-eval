import pytest


@pytest.fixture(autouse=True, scope='session')
def _environment(request):
    """Adds the endpoint info to the HTML report."""
    endpoint = request.config.option.endpoint
    request.config._environment.append(
        ('HGVS Endpoint', endpoint),
    )


def pytest_generate_tests(metafunc):
    if 'endpoint' in metafunc.fixturenames:
        endpoint = metafunc.config.option.endpoint
        metafunc.parametrize('endpoint', [endpoint])


def pytest_report_header(config):
    return "HGVS Endpoint: {}".format(config.option.endpoint)


def pytest_addoption(parser):
    parser.addoption("--endpoint",
                     help="Set the HGVS server endpoint")
