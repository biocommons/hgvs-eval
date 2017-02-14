import pytest
import pkg_resources
import csv
import hashlib


@pytest.fixture(autouse=True, scope='session')
def _environment(request):
    """Adds the endpoint info to the HTML report."""
    endpoint = request.config.option.endpoint
    request.config._environment.append(
        ('HGVS Endpoint', endpoint),
    )


@pytest.fixture(scope='session')
def endpoint(request):
    return request.config.option.endpoint


def pytest_report_header(config):
    return "HGVS Endpoint: {}".format(config.option.endpoint)


def pytest_generate_tests(metafunc):
    """Adds `endpoint` to each test function."""
    def _id(arg):
        return '_'.join([
            arg['feature'],
            arg['operation'],
            arg['name'],
	    arg['input']
        ])

    if 'criteria' in metafunc.fixturenames:
        criterias = []
        fname = pkg_resources.resource_filename(
            __name__, 'data/hgvs_eval_criteria_tests.tsv'
        )

        with open(fname, 'rb') as f:
            infile = csv.reader(f, delimiter='\t')
            header = None
            for row in infile:
                if not header:
                    header = row
                    continue
                if row[0].startswith("#"):
                    continue
                criterias.append(
                    dict(zip(header, row))
                )

        metafunc.parametrize(
            'criteria',
            criterias,
            indirect=False,
            ids=_id,
            scope=None
        )


def pytest_addoption(parser):
    parser.addoption(
        "--endpoint",
        help="Set the endpoint for the target HGVS server")
