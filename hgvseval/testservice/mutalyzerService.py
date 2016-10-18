from interface import HGVSTestService
from suds.client import Client


class MutalyzerService(HGVSTestService):
    def __init__(self):
        pass

    def info(self):
        pass

    def project_g_to_t(input_hgvs):
        url = 'https://mutalyzer.nl/services/?wsdl'
        c = Client(url, cache=None)
        o = c.service

        # as of 20161017 only hg19 is supposed by mutalyzer SOAP
        r = o.numberConversion(variant=input_hgvs, build='hg19')

        return [str(hgvs) for hgvs in r.string]


    def project_t_to_g(input_hgvs):
        url = 'https://mutalyzer.nl/services/?wsdl'
        c = Client(url, cache=None)
        o = c.service

        # as of 20161017 only hg19 is supposed by mutalyzer SOAP
        r = o.numberConversion(variant=input_hgvs, build='hg19')

        return [str(hgvs) for hgvs in r.string]


    def project_c_to_p(input_hgvs):
        pass

    def project_n_to_c(input_hgvs):
        pass

    def project_c_to_n(input_hgvs):
        pass

    def rewrite(input_hgvs):
        pass
