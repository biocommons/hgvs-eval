from interface import HGVSTestService
import hgvs.dataproviders.uta
import hgvs.parser
import hgvs.variantmapper
import hgvs.normalizer

class BiocommonsService(HGVSTestService):
    hp = hgvs.parser.Parser()
    hdp = hgvs.dataproviders.uta.connect()
    vm_GRCh37_splign =  hgvs.variantmapper.VariantMapper(hdp,
                                    replace_reference=True)
    
    hn = hgvs.normalizer.Normalizer(hdp)
    
    def __init__(self):
        pass
    
    def info(self):
        pass

    def project_t_to_g(self, hgvs_string, ac):
        var_t = BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        var_g = BiocommonsService.vm_GRCh37_splign.t_to_g(var_t, ac, alt_aln_method='splign')
        return var_g

    def project_g_to_t(self, hgvs_string, ac):
        var_g = BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        var_t = BiocommonsService.vm_GRCh37_splign.g_to_t(var_g, ac, alt_aln_method='splign')
        return var_t

    def project_c_to_p(self, hgvs_string):
        var_c = BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        var_p = BiocommonsService.vm_GRCh37_splign.c_to_p(var_c)
        return var_p

    def rewrite(self, hgvs_string):
        curr_var =  BiocommonsService.hp.parse_hgvs_variant(hgvs_string)
        norm_var = BiocommonsService.hn.normalize(curr_var)
        return norm_var

    def validate(self, hgvs_string):
        # ability to rewrite without exception being used as proxy for validate     
        try:
            self.rewrite(hgvs_string)
            return True
        except Exeption:
            return False
        

    
