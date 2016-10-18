import json

# our generated code
# generate via `$protoc hgvs.proto  --python_out=./`
import hgvs_pb2 as pb

from flask import Flask
from flask import request
from flask import render_template
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse
from google.protobuf.json_format import ParseDict

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
    resp = _createInfoResponse()
    resp.package_version = 'dummy-package-version'  # TODO - silly impl
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


@app.route('/project_t_to_g', methods=['POST'])
def project_t_to_g():
    """projects transcript (c. or n.) variant hgvs_string onto genomic
    sequence specified by ac, returning g. hgvs string
    Transcripts may be coding or non-coding.
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
    req = _getProjectionRequest()
    resp = _createProjectionResponse(hgvs_string='todo')  # TODO - silly impl
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
    req = Parse(request.data, pb.HGVSProjectionRequest())
    # print MessageToJson(req)
    return req


def _createParseResponse(start=None, end=None, alt=None):
    """
    create a HGVSParseResponse from the parameters
    """
    resp = pb.HGVSProjectionResponse()
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
    resp = pb.HGVSProjectionResponse()
    if hgvs_string:
        resp.hgvs_string = hgvs_string
    # print MessageToJson(resp)
    return resp


def _createInfoResponse(package_version=None,
                        rest_api_version=None,
                        eval_version=None,
                        timestamp=None,
                        nomenclature_version=None):
    """
    create a HGVSInfoResponse from the parameters
    """
    resp = pb.HGVSInfoResponse()
    if package_version:
        resp.package_version = package_version
    if rest_api_version:
        resp.rest_api_version = rest_api_version
    if eval_version:
        resp.eval_version = eval_version
    if timestamp:
        resp.timestamp = timestamp
    if nomenclature_version:
        resp.nomenclature_version = nomenclature_version
    # print MessageToJson(resp)
    return resp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # TODO - add config class
