import hgvseval
from .interface import HGVSTestService

import hgvs.dataproviders.uta
import hgvs.parser
import hgvs.variantmapper
import hgvs.normalizer
import hgvs.validator
import datetime

class BiocommonsService(HGVSTestService):
    hp = hgvs.parser.Parser()
    hdp = hgvs.dataproviders.uta.connect()
    vm = hgvs.variantmapper.VariantMapper(hdp)
    hn = hgvs.normalizer.Normalizer(hdp)
    val = hgvs.validator.Validator(hdp)

    def __init__(self):
        pass
    
    def info(self):
        return {
            "package_version": hgvs.__version__,
            "rest_api_version": None,
            "eval_version": hgvseval.__version__,
            "timestamp": '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()),
            #"nomenclature_version": 'yeah, right',
            }

    def project_t_to_g(self, hgvs_string, ac):
        var_t = BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        var_g = BiocommonsService.vm.t_to_g(var_t, ac)
        return str(var_g)

    def project_g_to_t(self, hgvs_string, ac):
        var_g = BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        var_t = BiocommonsService.vm.g_to_t(var_g, ac)
        return str(var_t)

    def project_c_to_p(self, hgvs_string):
        var_c = BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        var_p = BiocommonsService.vm.c_to_p(var_c)
        return str(var_p)

    def project_c_to_n(self, hgvs_string):
        var_c = BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        var_n = BiocommonsService.vm.c_to_n(var_c)
        return str(var_n)

    def project_n_to_c(self, hgvs_string):
        var_n = BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        var_c = BiocommonsService.vm.n_to_c(var_n)
        return str(var_c)

    def rewrite(self, hgvs_string):
        curr_var =  BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        norm_var = BiocommonsService.hn.normalize(curr_var)
        return str(norm_var)

    def validate(self, hgvs_string):
	try:
	    curr_var = BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
	    validate_var = BiocommonsService.val.validate(curr_var)
	    return str(validate_var)
	except Exception:
	    return 'False'

