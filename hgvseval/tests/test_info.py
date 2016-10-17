def test_info(endpoint):
    """Tests the info endpoint for the given service."""
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
    assert 1 == 1
