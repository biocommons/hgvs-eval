import requests
import json
from urlparse import urljoin


def test_info(endpoint):
    """Tests the info endpoint for the given service."""
    url = urljoin(endpoint, 'info')
    print "Testing HGVS service info endpoint on: {}".format(url)
    res = requests.get(url)
    print res.json()
    assert 1 == 1


def test_criteria(endpoint, criteria):
    """Criteria contains the params necessary to run each HGVS eval test.

    criteria: {
            'name': 'c_ins_to_dup',
            'tags': 'hgvs_c|ins|dup',
            'feature': 'formatting',
            'output_accepted': 'NM_005813.3:c.2673dupA|NM_005813.3:c.2673dup',
            'output_preferred': 'NM_005813.3:c.2673dup',
            'input': 'NM_005813.3:c.2673insA',
            'operation': 'rewrite',
            'test_source': '',
            'data': 'RefSeq',
            'varnomen_reference': '',
            'description': 'Tests ...'
        }
    """
    url = urljoin(endpoint, criteria['operation'])
    print "Testing HGVS operation on: {}".format(url)
    res = requests.post(
        url,
        data=json.dumps({
            'ac': criteria['output_accepted'].split(':')[0],
            'hgvsString': criteria['input']
        }))
    print res.json()
