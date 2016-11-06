hgvs-eval
!!!!!!!!!

*Automated evaluation suite to assess tools that manipulate
HGVS-formatted variants.*


Overview
@@@@@@@@

The hgvs-eval package provides an objective set of tests to evaluate
features provided by tools that manipulate HGVS-formatted variants.
The package envisions two users: 1) tool users who wish to identify a
tool for their use case; and 2) developers who would like additional
function tests.


It assesses the following features:

* Transcript source: NCBI/RefSeq, ENST, LRG

* Variant types: SNV, MNV, del, ins, delins

* Validation and Parsing: 

* Sequence Projections: Converting g. ⟺ c., g. ⟺ n., c. ⟹ p.

* Special cases: A few special features are assessed, including:

  * Correct projection in the presence of genome-transcript indels
  * Frameshifts include predicted distance to termination



Components
@@@@@@@@@@

* Test definitions -- a TSV file with inputs and expected output
* Test server -- the REST service that wraps the package being tested
* Test client -- runs tests (from test definitions) against the test server

This package currently includes all three components.

The test client is written in Python.

A test server may be written in any language appropriate for the
package being tested.

**TODO::** Write up REST interface specs as rst for inclusion in repo.


Quick start
@@@@@@@@@@@

These instructions assume that the client and server use the same
virtual environment.  The client and server may use different virtual
environments, or even different languages.

Download the package and prepare your environment::

  $ git clone https://github.com/biocommons/hgvs-eval.git
  $ cd hgvs-eval
  $ make devready
  $ source venv/bin/activate

If you have local instances of UTA and seqrepo, enable them with::

  (values will depend on your setup)
  $ export UTA_DB_URL=postgresql://anonymous@localhost/uta_dev/uta_20160908
  $ export HGVS_SEQREPO_DIR=/usr/local/share/seqrepo/20161024

Launch the REST service for biocommons/hgvs::

  $ python app.py &

A quick test::

  $ curl -d hgvs_string="NC_000020.10:g.278701_278703delGGC" -d ac=NM_033089.6  http://0.0.0.0:8000/project_g_to_t

Run the test suite (client), with output to HTML and JSON::

  $ hgvs-eval --html report.html --json report.json http://0.0.0.0:8000/

