from biocommonsService import BiocommonsService


my_biocommons_hgvs = BiocommonsService()

print "t_to_g: " + str(my_biocommons_hgvs.project_t_to_g("NM_001637.3:c.1582G>A", "NC_000007.13"))
print "g_to_t: " + str(my_biocommons_hgvs.project_g_to_t("NC_000007.13:g.36561662C>T", "NM_001637.3"))
print "c_to_p: " + str(my_biocommons_hgvs.project_c_to_p("NM_001637.3:c.1582G>A"))
print "norm: " + str(my_biocommons_hgvs.rewrite("NM_001637.3:c.1582G>A"))
print "validate: " + str(my_biocommons_hgvs.validate("NM_001637.3:c.1582G>A"))







