#!/bin/bash

# generate swagger documentation from protobuf using grpc support
# setup: see https://github.com/grpc-ecosystem/grpc-gateway#usage

protoc -I/usr/local/include -I.  -I$GOPATH/src  \
  -I$GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
  -I../hgvseval  \
  --swagger_out=logtostderr=true:../ ../hgvseval/messages.proto
