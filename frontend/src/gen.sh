#! /bin/sh
python -m grpc_tools.protoc -I. --python_out=generated/ --grpc_python_out=generated/ plagiarism_detection.proto