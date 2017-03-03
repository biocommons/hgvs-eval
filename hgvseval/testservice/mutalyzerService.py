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


    def project_g_to_t(input_hgvs):
        # as of 20161017 only hg19 is supposed by mutalyzer SOAP
        # numberConversion - converts I{c.} to I{g.} and vice versa
        r = MutalyzerService.o.numberConversion('hg19', input_hgvs)
        for hgvs in r.string:
            print hgvs
        #return [str(hgvs) for hgvs in r.string]


    def project_t_to_g(input_hgvs):
        # as of 20161017 only hg19 is supposed by mutalyzer SOAP
        r = MutalyzerService.o.numberConversion('hg19', input_hgvs)
        for hgvs in r.string:
            print hgvs
        #return [str(hgvs) for hgvs in r.string]


    def project_c_to_p(input_hgvs):
	# Should the same output given by different methods be compared?
	# Ex. transcripts given by runMutalyzer and numberConversion
        r = MutalyzerService.o.runMutalyzer(input_hgvs)
	for hgvs in r.proteinDescriptions.string:
	    print hgvs 


    def project_n_to_c(input_hgvs):
        pass

    def project_c_to_n(input_hgvs):
        pass

    def rewrite(input_hgvs):
        pass
