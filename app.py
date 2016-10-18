import logging

from flask import Flask, request
from google.protobuf.json_format import MessageToJson, Parse, ParseDict

import hgvseval.messages_pb2 as hm
from hgvseval.testservice.biocommonsService import BiocommonsService

logger = logging.getLogger(__name__)
bs = BiocommonsService()
app = Flask(__name__)


@app.route('/info', methods=['GET'])
def info():
    """ implements:
    service HGVSInfoService {
      rpc GetHGVSInfo(HGVSInfoRequest)
          returns (HGVSInfoResponse);
    }
    $ curl http://localhost:8000/info
    {
      "packageVersion": "dummy-package-version"
    }
    """
    resp = ParseDict(bs.info(), hm.HGVSInfoResponse())
    return MessageToJson(resp)


@app.route('/validate', methods=['POST'])
def validate():
    """ implements:
        service HGVSProjectionService {
          rpc GetHGVSValidation(HGVSProjectionRequest)
              returns (HGVSProjectionResponse);
        }
        $ curl -H "Content-Type: application/json" \
            -XPOST http://localhost:8000/validate \
            -d '{"ac": "test-ac-validate", "hgvsString": "test-hgvs-string"}'
        {
          "hgvsString": "todo"
        }
    """
    req = _getProjectionRequest()
    resp = _createProjectionResponse(hgvs_string='todo')  # TODO - silly impl
    return MessageToJson(resp)


@app.route('/parse', methods=['POST'])
def parse():
    """ implements:
        service HGVSProjectionService {
          rpc GetHGVSParse(HGVSProjectionRequest)
              returns (HGVSProjectionResponse);
        }
        $ curl -H "Content-Type: application/json" \
            -XPOST http://localhost:8000/parse \
            -d '{"ac": "test-ac-parse", "hgvsString": "test-hgvs-string"}'
        {
          "hgvsString": "todo"
        }
    """
    req = _getProjectionRequest()
    resp = _createProjectionResponse(hgvs_string='todo')  # TODO - silly impl
    return MessageToJson(resp)


@app.route('/rewrite', methods=['POST'])
def rewrite():
    """ implements:
        service HGVSProjectionService {
          rpc GetHGVSRewrite(HGVSProjectionRequest)
              returns (HGVSProjectionResponse);
        }
        $ curl -H "Content-Type: application/json" -XPOST \
            http://localhost:8000/rewrite \
            -d '{"ac": "test-ac-rewrite", "hgvsString": "test-hgvs-string"}'
        {
          "hgvsString": "todo"
        }
    """
    req = _getProjectionRequest()
    resp = _createProjectionResponse(hgvs_string='todo')  # TODO - silly impl
    return MessageToJson(resp)


@app.route('/project_g_to_t', methods=['POST'])
def project_g_to_t():
    """projects g. variant hgvs_string onto transcript sequence
    specified by ac, returning a c. or n. hgvs string
    Transcripts may be coding or non-coding.
    """
    
    hgvs_string = request.form.get("hgvs_string")
    ac = request.form.get("ac")
    print("project_g_to_t({}, {})".format(hgvs_string, ac))
    hgvs_string = bs.project_g_to_t(hgvs_string=hgvs_string, ac=ac)
    resp = _createProjectionResponse(hgvs_string=hgvs_string)
    return MessageToJson(resp)



@app.route('/project_t_to_g', methods=['POST'])
def project_t_to_g():
    """projects transcript (c. or n.) variant hgvs_string onto genomic
    sequence specified by ac, returning g. hgvs string
    Transcripts may be coding or non-coding.
    """
    hgvs_string = bs.project_t_to_g(hgvs_string=request["hgvs_string"], ac=request["ac"])
    resp = _createProjectionResponse(hgvs_string=hgvs_string)
    return MessageToJson(resp)

@app.route('/project_c_to_p', methods=['POST'])
def project_c_to_p():
    """projects c. hgvs_string onto corresponding
    protein sequence, returning a p. hgvs string.
    Transcripts may be coding or non-coding.
    """
    req = _getProjectionRequest()
    resp = _createProjectionResponse(hgvs_string='todo')  # TODO - silly impl
    return MessageToJson(resp)


def _getProjectionRequest():
    """
    create a HGVSProjectionRequest from the request
    """
    req = Parse(request.data, hm.HGVSProjectionRequest())
    # print MessageToJson(req)
    return req


def _createParseResponse(start=None, end=None, alt=None):
    """
    create a HGVSParseResponse from the parameters
    """
    resp = hm.HGVSProjectionResponse()
    if start is not None:
        resp.pos.start = start
        resp.pos.end = end
    if alt:
        resp.alt = alt
    # print MessageToJson(resp)
    return resp


def _createProjectionResponse(hgvs_string=None):
    """
    create a HGVSProjectionResponse from the parameters
    """
    resp = hm.HGVSProjectionResponse()
    if hgvs_string:
        resp.hgvs_string = hgvs_string
    # print MessageToJson(resp)
    return resp



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # TODO - add config class
