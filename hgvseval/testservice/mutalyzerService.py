from interface import HGVSTestService
from suds.client import Client
import datetime

class MutalyzerService(HGVSTestService):
    url = 'https://mutalyzer.nl/services/?wsdl'
    c = Client(url, cache=None)
    o = c.service

    def __init__(self):
        pass

    def info(self):
        info = MutalyzerService.o.info()
        # This needs to match HGVSInfoResponse
        return {
            "package_version": info.version,
            #"Tool_Release_Date": info.releaseDate,
            "timestamp" : '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()),
            "nomenclature_version": info.nomenclatureVersion,
        }


    def project_g_to_t(self, input_hgvs):
        # as of 20161017 only hg19 is supposed by mutalyzer SOAP
        # numberConversion - converts I{c.} to I{g.} and vice versa
        r = MutalyzerService.o.numberConversion('hg19', input_hgvs)
        hgvs_t = ",".join(r.string) 
        return hgvs_t       
        #return [str(hgvs) for hgvs in r.string]


    def project_t_to_g(self, input_hgvs):
        # as of 20161017 only hg19 is supposed by mutalyzer SOAP
        r = MutalyzerService.o.numberConversion('hg19', input_hgvs)
        return [str(hgvs) for hgvs in r.string]


    def project_c_to_p(self, input_hgvs):
	# Should the same output given by different methods be compared?
	# Ex. transcripts given by runMutalyzer and numberConversion
        r = MutalyzerService.o.runMutalyzer(input_hgvs)
        return [str(hgvs) for hgvs in r.proteinDescriptions.string]


    def project_n_to_c(self, input_hgvs):
        # numberConversion - converts I{c.} to I{g.} and vice versa
        r = MutalyzerService.o.numberConversion('hg19', input_hgvs)
        return [str(hgvs) for hgvs in r.string]


    def project_c_to_n(self, input_hgvs):
        # numberConversion - converts I{c.} to I{g.} and vice versa
        r = MutalyzerService.o.numberConversion('hg19', input_hgvs)
        return [str(hgvs) for hgvs in r.string]


    def rewrite(self, input_hgvs):
        pass


    def validate(self, input_hgvs):
        # There is no validate method in Mutalyzer
	# checkSyntax or runMutalyzer is used to check semantics
	# Do we test this?
	pass

'''
        curr_var = input_hgvs
	r = MutalyzerService.o.runMutalyzer(input_hgvs)
        if curr_var == returned_hgvs:
	    return 'True'
	else:
	    return 'False'
 
'''

'''
# For testing mutalyzerService.py
if __name__ == '__main__':
    mut = MutalyzerService()
    print mut.project_g_to_t('NC_000020.10:g.278701_278703delGGC')
    print mut.project_g_to_t('NC_000023.10:g.73501562T>C')
    print mut.project_t_to_g('NM_001135021.1:c.794T>C')
    print mut.project_c_to_p('NM_033089.6:c.471_473delGGC')
    print mut.project_n_to_c('NM_033089.6:n.495_497delGGC')
'''
