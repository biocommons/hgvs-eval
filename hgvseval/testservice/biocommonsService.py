import hgvseval
from .interface import HGVSTestService

import hgvs.dataproviders.uta
import hgvs.parser
import hgvs.variantmapper
import hgvs.normalizer


class BiocommonsService(HGVSTestService):
    hp = hgvs.parser.Parser()
    hdp = hgvs.dataproviders.uta.connect()
    vm = hgvs.variantmapper.VariantMapper(hdp)
    hn = hgvs.normalizer.Normalizer(hdp)
    
    def __init__(self):
        pass
    
    def info(self):
        return {
            "package_version": hgvs.__version__,
            "rest_api_version": None,
            "eval_version": hgvseval.__version__,
            "timestamp": None,
            "nomenclature_version": 'yeah, right',
            }

    def project_t_to_g(self, hgvs_string, ac):
        var_t = BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        var_g = BiocommonsService.vm.t_to_g(var_t, ac, alt_aln_method='splign')
        return str(var_g)

    def project_g_to_t(self, hgvs_string, ac):
        var_g = BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        var_t = BiocommonsService.vm.g_to_t(var_g, ac, alt_aln_method='splign')
        return str(var_t)

    def project_c_to_p(self, hgvs_string):
        var_c = BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        var_p = BiocommonsService.vm.c_to_p(var_c)
        return str(var_p)

    def project_c_to_n(self, hgvs_string):
        var_c = BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        var_n = BiocommonsService.vm.c_to_n(var_c)
        return str(var_n)

    def rewrite(self, hgvs_string):
        curr_var =  BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        norm_var = BiocommonsService.hn.normalize(curr_var)
        return str(norm_var)

    def validate(self, hgvs_string):
        # ability to rewrite without exception being used as proxy for validate     
        try:
            self.rewrite(hgvs_string)
            return True
        except Exeption:
            return False
