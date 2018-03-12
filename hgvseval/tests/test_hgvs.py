import requests
import json
from urlparse import urljoin

def test_info(endpoint):
    """Tests the info endpoint for the given service."""
    url = urljoin(endpoint, 'info')
    print "Testing HGVS service info endpoint on: {}".format(url)
    res = requests.get(url)
    #print res.json() # prints to command line but not to report
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
    
    res = requests.post( # This is sending the data to test each test case
        url,
        data={
            'ac': criteria['output_accepted'].split(':')[0], # Gets 1st accession number encountered
            'hgvs_string': criteria['input'],
            'build':criteria['data']
        })

    # TODO: Understand why this doesn't have the modified HGVS variants I processed in mutalyzerService.py
    # This prints out 'No output from tool'...So why can't it print out the reformatted HGVS vars?
    #print res.json() # prints result from tool to command line but not to report
    result = res.json()
    result_hgvs = result['hgvsString']
    #print(result_hgvs) # This is just what is returned from the test  

    passed = False
    # TODO: Implement a check or somehow gracefully skip over Mutalyzer tests that I know 
    #       are going to fail (ex. g. run through runMutalyzer in rewrite or validate)
    #       1. if result_hgvs is not 'No output from tool': (All test cases have this output)
    #       2. pytest skip?
    hgvs_vars = {}
    if "," in result_hgvs:
        my_hgvs_arr = result_hgvs.split(',')
        for h in my_hgvs_arr:
            hgvs_vars[h] = 1
        #print hgvs_vars
        ac_list = criteria['output_accepted'].split('|')
        for accepted_output in ac_list:
            #print accepted_output
            if accepted_output in hgvs_vars:
                passed = True
    else:
        ac_list = criteria['output_accepted'].split('|')
        for accepted_output in ac_list:
            if(result_hgvs == accepted_output):
                passed = True

    assert passed
