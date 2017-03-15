import logging

from flask import Flask, request,  Response
from flask_cors import CORS

from google.protobuf.json_format import MessageToJson, Parse, ParseDict
import json
import hgvseval.messages_pb2 as hm
import os

import sys
import argparse
import importlib

logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)

tools = {
    'Biocommons':['hgvseval.testservice.biocommonsService', 'BiocommonsService'],
    'Mutalyzer':['hgvseval.testservice.mutalyzerService', 'MutalyzerService']
}

tool = sys.argv[1]
if tool in tools:
    package = tools[tool][0]
    name = tools[tool][1]
    my_module = importlib.import_module(package)
    class_ = getattr(my_module, name)
    service = class_()


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
    resp = ParseDict(service.info(), hm.HGVSInfoResponse())
    return MessageToJson(resp) 
    '''
    resp = ParseDict(bs.info(), hm.HGVSInfoResponse())
    mut_resp = ParseDict(mut.info(), hm.HGVSInfoResponse())
    tools_info_resp = [resp, mut_resp]
    for i in range(0, len(tools_info_resp)):
        tools_info_resp[i] = json.loads(MessageToJson(tools_info_resp[i]))
    return json.dumps(tools_info_resp)
    # This does the same thing as the for loop but in 1 line
    #return json.dumps(map(lambda r: json.loads(MessageToJson(r)), tools_info_resp))
    '''    


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
    hgvs_string = request.form.get("hgvs_string")
    hgvs_string = service.validate(hgvs_string=hgvs_string)
    resp = _createProjectionResponse(hgvs_string=hgvs_string)
    return MessageToJson(resp)


@app.route('/parse', methods=['POST'])
def parse():
    """Breaks down HGVS expression into parts

	implements:
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

        VMC Data Model?
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
    hgvs_string = request.form.get("hgvs_string")
    hgvs_string = service.rewrite(hgvs_string=hgvs_string)
    #req = _getProjectionRequest()
    resp = _createProjectionResponse(hgvs_string=hgvs_string)
    return MessageToJson(resp)


@app.route('/project_g_to_t', methods=['POST'])
def project_g_to_t():
    """projects g. variant hgvs_string onto transcript sequence
    specified by ac, returning a c. or n. hgvs string
    Transcripts may be coding or non-coding.
    """
    hgvs_string = request.form.get("hgvs_string")
    ac = request.form.get("ac")
    #print("project_g_to_t({}, {})".format(hgvs_string, ac)) # where does this print?
    hgvs_string = service.project_g_to_t(hgvs_string=hgvs_string, ac=ac)
    resp = _createProjectionResponse(hgvs_string=hgvs_string)
    return MessageToJson(resp)


@app.route('/project_t_to_g', methods=['POST'])
def project_t_to_g():
    """projects transcript (c. or n.) variant hgvs_string onto 
    genomic sequence specified by ac, returning g. hgvs string
    Transcripts may be coding or non-coding.
    """
    hgvs_string = request.form.get("hgvs_string")
    ac = request.form.get("ac")
    hgvs_string = service.project_t_to_g(hgvs_string=hgvs_string, ac=ac)
    resp = _createProjectionResponse(hgvs_string=hgvs_string)
    return MessageToJson(resp)


@app.route('/project_c_to_p', methods=['POST'])
def project_c_to_p():
    """projects c. hgvs_string onto corresponding
    protein sequence, returning a p. hgvs string.
    Transcripts may be coding or non-coding.
    """
    hgvs_string = request.form.get("hgvs_string")
    hgvs_string = service.project_c_to_p(hgvs_string=hgvs_string)
    resp = _createProjectionResponse(hgvs_string=hgvs_string)
    return MessageToJson(resp)


@app.route('/project_c_to_n', methods=['POST'])
def project_c_to_n():
    """projects c. hgvs_string onto non-coding
    sequence, returning n. hgvs string
    """
    hgvs_string = request.form.get("hgvs_string")
    hgvs_string = service.project_c_to_n(hgvs_string=hgvs_string)
    resp = _createProjectionResponse(hgvs_string=hgvs_string)
    return MessageToJson(resp)


@app.route('/project_n_to_c', methods=['POST'])
def project_n_to_c():
    """projects n. hgvs_string onto coding
    sequence, returning c. hgvs string
    """
    hgvs_string = request.form.get("hgvs_string")
    hgvs_string = service.project_n_to_c(hgvs_string=hgvs_string)
    resp = _createProjectionResponse(hgvs_string=hgvs_string)
    return MessageToJson(resp)


@app.route("/api")
def getSwaggerJson():
    json_file = open(os.path.join(
                     "./", "messages.swagger.json"), "r")
    json = json_file.read()
    json_file.close()
    resp = Response(response=json,
                    status=200,
                    mimetype="application/json")
    return resp


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
    parser = argparse.ArgumentParser()
    parser.add_argument('tool', help='Name of tool to test. Supported tools: Biocommons, Mutalyzer')
    args = parser.parse_args()
    app.run(debug=True, host='0.0.0.0', port=8000)  # TODO - add config class

