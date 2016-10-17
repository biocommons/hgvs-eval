from interface import HGVSTestService
import hgvs.dataproviders.uta
import hgvs.parser
import hgvs.variantmapper
import hgvs.normalizer

class Biocommons_hgvs(HGVSTestService):
    hp = hgvs.parser.Parser()
    hdp = hgvs.dataproviders.uta.connect()
    evm_GRCh37_splign =  hgvs.variantmapper.EasyVariantMapper(hdp,
                                    assembly_name='GRCh37', alt_aln_method='splign',
                                    replace_reference=True)
    
    hn = hgvs.normalizer.Normalizer(hdp)
    
    def __init__(self):
        pass
    
    def info(self):
        pass

    def project_t_to_g(self, hgvs_string):
        var_t = Biocommons_hgvs.hp.parse_hgvs_variant(hgvs_string)
        var_g = Biocommons_hgvs.evm_GRCh37_splign.t_to_g(var_t)
        return var_g

    def project_g_to_t(self, hgvs_string, ac):
        var_g = Biocommons_hgvs.hp.parse_hgvs_variant(hgvs_string)
        var_t = Biocommons_hgvs.evm_GRCh37_splign.g_to_t(var_g, ac)
        return var_t

    def project_c_to_p(self, hgvs_string):
        var_c = Biocommons_hgvs.hp.parse_hgvs_variant(hgvs_string)
        var_p = Biocommons_hgvs.evm_GRCh37_splign.c_to_p(var_c)
        return var_p

    def rewrite(self, hgvs_string):
        curr_var =  Biocommons_hgvs.hp.parse_hgvs_variant(hgvs_string)
        norm_var = Biocommons_hgvs.hn.normalize(curr_var)
        return norm_var

    def validate(self, hgvs_string):
        # ability to rewrite without exeception being used as proxy for validate     
        try:
            self.rewrite(hgvs_string)
            return True
        except Exeption:
            return False
        

    
