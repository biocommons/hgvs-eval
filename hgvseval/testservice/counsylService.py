import hgvseval
from interface import HGVSTestService

import pyhgvs as hgvs
import pyhgvs.utils as hgvs_utils
from pygr.seqdb import SequenceFileDB
from pkg_resources import get_distribution
import datetime
import os

# Using biocommons hgvs to get transcript for project_g_to_t
#import hgvs.dataproviders.uta
#import hgvs.variantmapper
#hdp = hgvs.dataproviders.uta.connect()
#vm = hgvs.variantmapper.EasyVariantMapper(hdp)

# TODO: file path can't be hardcoded
genome = SequenceFileDB('/media/sf_shared_folder_vm/counsyl_files/ucsc.hg19.fasta')

class CounsylService(HGVSTestService):

    def __init__(self):
        # TODO: file path can't be hardcoded
        with open('/media/sf_shared_folder_vm/counsyl_files/transcripts.gp') as infile:
            self.transcripts = hgvs_utils.read_transcripts(infile)

    def get_transcript(self, name):
        return self.transcripts.get(name)

    def info(self):
        pkg = get_distribution('pyhgvs')
        return {
            "package_version": pkg.version,
            "rest_api_version": None,
            "eval_version": hgvseval.__version__,
            "timestamp": '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()),
            #"nomenclature_version":,
            }

    def project_t_to_g(self, hgvs_string, ac):
        chrom, offset, ref, alt = hgvs.parse_hgvs_name(hgvs_string, genome, get_transcript=self.get_transcript)
        transcript = self.get_transcript(ac)
        # variant_to_hgvs_name() and format_hgvs_name() give the same output
        #var_g = hgvs.variant_to_hgvs_name(chrom, offset, ref, alt, genome, transcript=None)
        # transcript=None or else it will print hgvs_string I passed in
        # TODO: Print HGVS annotation with chr accession number
	var_g = hgvs.format_hgvs_name(chrom, offset, ref, alt, genome, transcript=None)
        return var_g.format()

    def project_g_to_t(self, hgvs_string, ac):
        # Need to provide the transcript OR call to another tool to get transcript      
        #chrom, offset, ref, alt = hgvs.parse_hgvs_name(hgvs_string, genome, get_transcript=self.get_transcript)
        # call to another tool to get transcript
        print hgvs_string
        print ac
        chrom, offset, ref, alt = hgvs.parse_hgvs_name(hgvs_string, genome, get_transcript=self.get_transcript)
        transcript = self.get_transcript(ac)
        var = hgvs.format_hgvs_name(chrom, offset, ref, alt, genome, transcript=None)
        return var.format()
        #return hgvs.HGVSName(hgvs_string)
        '''
        trx = vm.relevant_transcripts(hgvs_string)
        transcript = self.get_transcript(trx)
        #cdna_coord = hgvs.genomic_to_cdna_coord(transcript, offset)
        var_t = hgvs.variant_to_hgvs_name(chrom, offset, ref, alt, genome, transcript)
        return var_t.format(use_gene=False)
        '''

    def project_c_to_p(self, hgvs_string):
        # Counsyl does not have this feature
        pass

    def project_n_to_c(self, hgvs_string):
        return "Feature not supported by Counsyl hgvs" 

    def project_c_to_n(self, hgvs_string):
        return "Feature not supported by Counsyl hgvs" 

    def rewrite(self, hgvs_string):
        # It might be better to call HGVSName instead because it gives you the transcript
        # but will this work for g. and p.?
        # get an example of a g. that can be rewritten
        # HGVSName() won't give me chrom and offset which I need for variant_to_hgvs_name
        # have the same problem where the transcript number is not found in file but chr is
        chrom, offset, ref, alt = hgvs.parse_hgvs_name(hgvs_string, genome, get_transcript=self.get_transcript)
        trx = hgvs.HGVSName(hgvs_string).transcript
        transcript = self.get_transcript(trx)
        hgvs_name = hgvs.variant_to_hgvs_name(chrom, offset, ref, alt, genome, transcript)
        return hgvs_name.format(use_gene=False)
        '''
        chrom, offset, ref, alt = hgvs.parse_hgvs_name(hgvs_string, genome, get_transcript=self.get_transcript)
        #TODO: Use regex to get ac
        transcript = self.get_transcript('NM_001166478.1')
        norm_var = hgvs.hgvs_normalize_variant(chrom, offset, ref, alt, genome, transcript)
        return hgvs.format_hgvs_name(chrom, offset, ref, alt, genome, transcript, use_gene=False)
        '''
        '''
        chrom, offset, ref, alt = hgvs.parse_hgvs_name(hgvs_string, genome, get_transcript=self.get_transcript)
        print chrom, offset, ref, alt
        transcript = self.get_transcript('NM_001166478.1')
        #chrom, offset, ref, [alt] = hgvs.normalize_variant(chrom, offset, ref, [alt], genome).variant
        #chrom, offset, ref, alt, mutation_type = hgvs_normalize_variant(chrom, offset, ref, alt, genome, transcript)
        norm_var = hgvs.normalize_variant(chrom, offset, ref, [alt], genome).variant
        #hgvs_norm_var = hgvs.hgvs_normalize_variant(chrom, offset, ref, alt, genome, transcript)
        #print chrom, offset, ref, [alt]
        return norm_var
        #return hgvs.format_hgvs_name(chrom, offset, ref, alt, genome, transcript, use_gene=False)
        '''

    def validate(self, hgvs_string):
        # This will most likely be the same as rewrite
        pass

    def parse(self, hgvs_string):
        try:
            var = hgvs.HGVSName(hgvs_string)
            if var.kind == 'c':
                parsed_var = { 
                    'location': {
                        'start': var.cdna_start,
                        'end': var.cdna_end,
                    },
                    'type': var.kind,
                    'replacement': var.alt_allele,
                    'seqref': var.prefix
                }
            else:
                parsed_var = { 
                    'location': {
                        'start': str(var.start),
                        'end': str(var.end),
                    },
                    'type': var.kind,
                    'replacement': var.alt_allele,
                    'seqref': var.prefix
                }
            #return parsed_var
            return 'True'
        except:
            #return "Counsyl HGVS supports g., c. and p. HGVS variants"
            return 'False'


if __name__=='__main__':
    c = CounsylService()
    print c.info()
    #print c.rewrite('NM_001166478.1:c.35_36insT')
    #print c.rewrite('NC_000006.11:g.49917122_49917123insA') #doesn't work because trx number not found in file  
    #print c.rewrite('chr6:g.49917122_49917123insA') 
    #print c.project_t_to_g('NM_001135021.1:c.794T>C', 'NM_001135021.1') #output: g.85616929T>C
    #print c.project_t_to_g('NM_001166478.1:c.35dup', 'NM_001166478.1')
    #print c.rewrite('NM_001166478.1:c.31dup')
    #print c.rewrite('NM_001166478.1:c.35_36insT')
    #print c.rewrite('NM_001166478.1:c.31del')
    #print c.rewrite('NC_000020.10:g.278689_278691delGGC') #didn't work
    #print c.rewrite('NC_000020.11:g.298048_298050delGGC') #didn't work
    #print c.rewrite('NC_000020.10:g.278701_278703del') #didn't work
    #print c.project_t_to_g('NM_003000.2:c.*159_*184delinsGAACCTGTTCCTTTACTTGCCCCAA', 'NG_012340.1')
    #print c.rewrite('NM_003002.3:c.274G>T')
    #print c.rewrite('NM_000492.3:c.1520_1522delTCT')
    #print c.rewrite('NC_000002.11:g.37480321_37480322insT') #didn't work
    #print c.rewrite('NC_000002.12:g.37253177_37253178insT') #didn't work
    #print c.rewrite('NM_005813.3:c.2672_2673insA')
    #print 'genomic del', c.parse('NC_000020.10:g.278701_278703delGGC')
    #print 'genomic', c.parse('NC_000023.10:g.73501562T>C')
    #print 'transcript', c.parse('NM_000352.4:c.215A>G')
    #print 'intronic transcript', c.parse('NM_000352.3:c.1630+1G>A')
    # the line below works because chr2 matches what is in ucsc.hg19.fasta 
    #print c.project_g_to_t('chr2:g.85616929T>C', 'NC_000002.11')
    # Doesn't like NP_001128495.1:p.(Leu265Ser)
    #print 'protein', c.parse('NP_001128495.1:p.Leu265Ser')
    # the line below doesn't work because NC_000002.11 is not in fasta
    #print c.project_g_to_t('NC_000002.11:g.85616929T>C', 'NC_000002.11')
    #print c.project_g_to_t('NC_000006.11:g.49917127dup', 'NC_000006.11')
    #print c.project_t_to_g('NM_003000.2:c.*159_*184delinsGAACCTGTTCCTTTACTTGCCCCAA','NM_003000.2')
    #print c.project_t_to_g('NM_003000.2:c.*159_*184delinsGAACCTGTTCCTTTACTTGCCCCAA','NG_012340.1')
    #print c.rewrite('chr2:g.37480321_37480322insT')
    #print c.rewrite('chr2:g.37480320_37480321insT')
    #print c.rewrite('chr2:g.37253177_37253178insT')
    #print c.rewrite('NM_005813.3:c.2672_2673insA')
    #print c.rewrite('NM_001197320.1:c.281C>T')
    #print c.project_t_to_g('NM_001197320.1:c.281C>T','NM_001197320.1')
    #print c.rewrite('NM_001197320.1:c.281A>T')
    #print c.rewrite('NP_689699.2:p.(G553E)') 
    #print c.rewrite('NM_002111.6:c.52CAG[36_39]')
    #print c.project_t_to_g('NM_001166478.1:c.35dup', 'NM_001166478.1')
