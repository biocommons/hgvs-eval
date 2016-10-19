hgvs-eval 
!!!!!!!!!

Automated evaluation suite to assess tools that manipulate HGVS formatted variants


Developers installation instructions::

  > virtualenv hgvseval-ve
  > source hgvseval-ve/bin/activate
  > git clone https://github.com/biocommons/hgvs-eval.git
  > cd hgvs-eval
  > make setup 
  > make develop


Launch REST service for biocommons/hgvs::

  > python app.py


Test the endpoint::

   curl \
   -d hgvs_string="NC_000020.10:g.278701_278703delGGC" \
   -d ac=NM_033089.6  \
   http://0.0.0.0:8000/project_g_to_t


----
