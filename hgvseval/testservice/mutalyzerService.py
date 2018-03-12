from interface import HGVSTestService
from suds.client import Client
import datetime
import re

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


    def project_g_to_t(self, hgvs_string, ac, build):
        # as of 20161017 only hg19 is supposed by mutalyzer SOAP
        # numberConversion - converts I{c.} to I{g.} and vice versa
        r = MutalyzerService.o.numberConversion('hg19', hgvs_string)
        hgvs_t = ",".join(r.string) 
        return hgvs_t       
        #return [str(hgvs) for hgvs in r.string]


    def project_t_to_g(self, hgvs_string, ac, build):
        # as of 20161017 only hg19 is supposed by mutalyzer SOAP
        r = MutalyzerService.o.numberConversion('hg19', hgvs_string)
        hgvs_g = ",".join(r.string) 
        return hgvs_g       
        #return [str(hgvs) for hgvs in r.string]


    def project_c_to_p(self, hgvs_string):
	# Should the same output given by different methods be compared?
	# Ex. transcripts given by runMutalyzer and numberConversion
        r = MutalyzerService.o.runMutalyzer(hgvs_string)
        hgvs_p = ",".join(r.proteinDescriptions.string) 
        return hgvs_p       
        #return [str(hgvs) for hgvs in r.proteinDescriptions.string]


    def project_n_to_c(self, hgvs_string):
        # numberConversion - converts I{c.} to I{g.} and vice versa
        r = MutalyzerService.o.numberConversion('hg19', hgvs_string)
        hgvs_c = ",".join(r.string) 
        return hgvs_c      
        #return [str(hgvs) for hgvs in r.string]


    def project_c_to_n(self, hgvs_string):
        # numberConversion - converts I{c.} to I{g.} and vice versa
        r = MutalyzerService.o.numberConversion('hg19', hgvs_string)
        hgvs_n = ",".join(r.string) 
        return hgvs_n       
        #return [str(hgvs) for hgvs in r.string]


    def rewrite(self, hgvs_string):
        #r = MutalyzerService.o.runMutalzyer(input_hgvs)
        # How would this know what type of hgvs variant it got(g.,c.,p.)? 
        r = MutalyzerService.o.runMutalyzer(hgvs_string)
        all_hgvs = []
        if hasattr(r, 'genomicDescription'):
            all_hgvs.append(r.genomicDescription)
        if r.proteinDescriptions is not None:
            all_hgvs.extend(r.proteinDescriptions.string)
        if r.transcriptDescriptions is not None:
            all_hgvs.extend(r.transcriptDescriptions.string)
        if not all_hgvs:
            all_hgvs_str = 'No output from tool'
        else:
            all_hgvs_str = ",".join(all_hgvs)
        return all_hgvs_str


    def validate(self, hgvs_string):
	# runMutalyzer (Run the Mutalyzer name checker)
        # How would this know what type of hgvs variant it got if we used runMutalyzer(g.,c.,p.)?
        # I could pull in all HGVS descriptions returned and iterate through them
        ''' 
        r = MutalyzerService.o.checkSyntax(hgvs_string)
        return str(r.valid)
        '''
        curr_var = hgvs_string
	r = MutalyzerService.o.runMutalyzer(hgvs_string)
        all_hgvs = {}
        hgvs_list = []
        # Going to assume this won't have any (). This might be a bad assumption.
        # Also assuming this is always a string
        if hasattr(r, 'genomicDescription'):
            #all_hgvs[r.genomicDescription] = 1
            hgvs_list.append(r.genomicDescription)
        if r.proteinDescriptions is not None:
            hgvs_list.extend(r.proteinDescriptions.string)
        if r.transcriptDescriptions is not None:
            hgvs_list.extend(r.transcriptDescriptions.string)
        if not hgvs_list:
            output = 'False'
        else:
            for h in hgvs_list:
                match = re.search(r, h)
                all_hgvs[match.group(1)+match.group(3)] = 1
            if curr_var in all_hgvs:
	        output = 'True'
	    else:
	        output = 'False'
        return output


    def parse(self, hgvs_string):
        # Mutalyzer does not have this feature
        return 'False'

'''
# For testing mutalyzerService.py
if __name__ == '__main__':
    mut = MutalyzerService()
    #print mut.info()
    #print mut.project_g_to_t('NC_000006.12:g.49949402C>A', 'NM_001166478.1', 'GRCh38') #Returns None and errors. Is that ok?
'''
