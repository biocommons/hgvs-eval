import abc


class HGVSTestService(object):
    @abc.abstractmethod
    def info(self):
        """returns dictionary of package info
        """
        pass


    @abc.abstractmethod
    def project_t_to_g(self, hgvs_string, ac):
        """projects transcript (c. or n.) variant hgvs_string onto 
	genomic sequence specified by ac, returning g. hgvs string

        Transcripts may be coding or non-coding.

        """
        pass


    @abc.abstractmethod
    def project_g_to_t(self, hgvs_string, ac):
        """projects g. variant hgvs_string onto transcript sequence
        specified by ac, returning a c. or n. hgvs string

        Transcripts may be coding or non-coding.

        """
        pass

    @abc.abstractmethod
    def project_c_to_p(self, hgvs_string):
        """projects c. hgvs_string onto corresponding
        protein sequence, returning a p. hgvs string.

        Transcripts may be coding or non-coding.

        """
        pass

    @abc.abstractmethod
    def project_c_to_n(self, hgvs_string):
        """projects c. hgvs_string onto non-coding sequence, 
	returning a n. hgvs string.

        """
        pass

    @abc.abstractmethod
    def project_n_to_c(self, hgvs_string):
        """projects n. hgvs_string onto corresponding
        coding sequence, returning a c. hgvs string.

        """
        pass

    @abc.abstractmethod
    def rewrite(self, hgvs_string):
        """normalize and rewrite hgvs_string in a canonical form"""
        pass


    @abc.abstractmethod
    def parse(self, hgvs_string):
        """parse hgvs_string and return json representation"""
        pass
                  

    @abc.abstractmethod
    def validate(self, hgvs_string):
        """parse and validate variant returning status and optional messages

        If the variant is valid, returns (True, []).

        If the variant is 
        messages). Status is True or False, and messages is a list of
        text messages explaining the failure.  messages should be
        empty if the status is True.

        """
        pass
