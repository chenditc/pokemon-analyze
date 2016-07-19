#!/usr/bin/python

from subprocess import Popen, PIPE

import base64
from bs4 import BeautifulSoup
import pandas

import POGOProtos_pb2



def remove_header(message_body):
    index = message_body.find("\r\n\r\n")
    protoc_buff = message_body[index+4:]
    return protoc_buff


def decode_response_envelope(protoc_buff):
    protoc_buff = remove_header(protoc_buff)
    message = POGOProtos_pb2.Networking.Envelopes.ResponseEnvelope()
    message.ParseFromString(protoc_buff)
    return message

def decode_request_envelope(protoc_buff):
    protoc_buff = remove_header(protoc_buff)
    message = POGOProtos_pb2.Networking.Envelopes.RequestEnvelope()
    message.ParseFromString(protoc_buff)
    return message

def decode_raw(protoc_buff):
    p = Popen(["protoc", "--decode_raw"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    result = p.communicate(protoc_buff)[0]
    return result

with open('./request_history', 'r') as input_file:
    xml_doc = input_file.read()
    soup = BeautifulSoup(xml_doc, 'xml')
    items = soup.items.find_all("item")


    for item in items:
        comment = item.comment.getText()
        url = item.url.getText()
        if "pgorelease.nianticlabs.com" not in url:
            continue

        request_base64 = item.request.getText()
        request = base64.b64decode(request_base64)
        response_base64 = item.response.getText()
        response = base64.b64decode(response_base64)

        request_body = decode_request_envelope(request) 
        response_body = decode_response_envelope(response)

        print "================================================="
        print("Comment: {0}".format(comment))
        print(request_body)
        print "================================================="
        print(response_body)
        print("-------------------------------------------------")
