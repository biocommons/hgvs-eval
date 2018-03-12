from interface import HGVSTestService
import requests
import datetime
import json

class VariationReporterService(HGVSTestService):
    url = 'https://www.ncbi.nlm.nih.gov/projects/SNP/VariantAnalyzer/var_rep.cgi'

    def __init__(self):
        pass

    def info(self):
        return {
            "package_version" : "1.4.1.9", #has to be hardcoded
            "timestamp" : '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        }

    def project_g_to_t(self, hgvs_string, ac, build):
        ref = build.split('|')[0]
        if ref == 'GRCh38':
            r = requests.post(self.url, data={'annot1': hgvs_string, 'source-assembly': 'GCF_000001405.33'})
        else:
            r = requests.post(self.url, data={'annot1': hgvs_string})
        report = r.text
        lines = report.splitlines()
        variants = lines[20:]
        all_hgvs_c = []
        for v in variants:
            # TODO: Add in NR_?
            if not v:
                continue
            all_hgvs_c.append(v.split("\t")[12])
        all_hgvs_c = [x for x in all_hgvs_c if x != '']
        unique_vars = set(all_hgvs_c)
        if len(unique_vars) == 1:
            for x in unique_vars:
                hgvs_c = x
        else:
            hgvs_c = ','.join(unique_vars)
        return hgvs_c

    def project_t_to_g(self, hgvs_string, ac, build):
        ref = build.split('|')[0]
        if ref == 'GRCh38':
            r = requests.post(self.url, data={'annot1': hgvs_string, 'source-assembly': 'GCF_000001405.33'})
        else:
            r = requests.post(self.url, data={'annot1': hgvs_string})
        report = r.text
        lines = report.splitlines()
        variants = lines[20:]
        all_hgvs_g = []
        for v in variants:
            if not v:
                continue
            # Might need to check these?
            #result = v.startswith(hgvs_string, 0, len(hgvs_string))
            #if v.startswith("NC_") == True:
                #all_hgvs_g.append(v.split("\t")[9])
            all_hgvs_g.append(v.split("\t")[9])
        all_hgvs_g = [x for x in all_hgvs_g if x != '']
        unique_vars = set(all_hgvs_g)
        if len(unique_vars) == 1:
            for x in unique_vars:
                hgvs_g = x
        else:
            hgvs_g = ','.join(unique_vars)
        return hgvs_g

    def project_c_to_p(self, hgvs_string):
        r = requests.post(self.url, data={'annot1': hgvs_string})
        report = r.text
        lines = report.splitlines()
        variants = lines[20:]
        all_hgvs_p = []
        for v in variants:
            if not v:
                continue
            all_hgvs_p.append(v.split("\t")[13])
        all_hgvs_p = [x for x in all_hgvs_p if x != '']
        unique_vars = set(all_hgvs_p)
        if len(unique_vars) == 1:
            for x in unique_vars:
                hgvs_p = x
        else:
            hgvs_p = ','.join(unique_vars)
        return hgvs_p

    def project_c_to_n(self, hgvs_string):
        # Decided to make this call Variation Reporter even though
        # it looks like it doesn't project c.to n.
        r = requests.post(self.url, data={'annot1': hgvs_string})
        report = r.text
        lines = report.splitlines()
        variants = lines[20:]
        all_hgvs_n = []
        for v in variants:
            if not v:
                continue
            all_hgvs_n.append(v.split("\t")[12])
        all_hgvs_n = [x for x in all_hgvs_n if x != '']
        unique_vars = set(all_hgvs_n)
        if len(unique_vars) == 1:
            for x in unique_vars:
                hgvs_n = x
        else:
            hgvs_n = ','.join(unique_vars)
        return hgvs_n

    def project_n_to_c(self, hgvs_string):
        r = requests.post(self.url, data={'annot1': hgvs_string})
        report = r.text
        lines = report.splitlines()
        variants = lines[20:]
        all_hgvs_c = []
        for v in variants:
            if not v:
                continue
            all_hgvs_c.append(v.split("\t")[12])
        all_hgvs_c = [x for x in all_hgvs_c if x != '']
        unique_vars = set(all_hgvs_c)
        if len(unique_vars) == 1:
            for x in unique_vars:
                hgvs_c = x
        else:
            hgvs_c = ','.join(unique_vars)
        return hgvs_c

    def rewrite(self, hgvs_string):
        # Variation Reporter does not have this feature
        pass

    def validate(self, hgvs_string):
        # Variation Reporter does not have this feature
        pass
    
    def parse (self, hgvs_string):
        # Variation Reporter does not have this feature
        return 'False'


'''
if __name__ == '__main__':
    vr = VariationReporterService()
    #print vr.info()
    #print vr.project_t_to_g('NR_028379.1:n.345A>G', 'NR_028379.1')
    #print vr.project_g_to_t('NC_000023.11:g.74281727T>C', 'NR_028379.1', 'GRCh38')
    #print vr.project_c_to_p('NM_033089.6:c.471_473delGGC')
    #print vr.project_t_to_g('NM_001166478.1:c.35dup', 'NM_001166478.1', 'GRCh38')
    #print vr.project_c_to_p('NM_001166478.1:c.35dup')
    #print vr.project_t_to_g('NM_003000.2:c.*159_*184delinsGAACCTGTTCCTTTACTTGCCCCAA', 'NM_003000.2', 'GRCh37')
    #print vr.project_g_to_t('NC_000002.11:g.37480321dup', 'NM_005813.4', 'GRCh37')
    #print vr.project_g_to_t('NC_000002.12:g.37253178dup', 'NM_005813.4', 'GRCh38')
    print vr.project_c_to_p('NM_012093.3:c.1606_1607insAATTT')
'''
