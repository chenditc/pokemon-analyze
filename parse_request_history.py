#!/usr/bin/python

from subprocess import Popen, PIPE

import base64
from bs4 import BeautifulSoup
import pandas

import POGOProtos_pb2

def remove_header(message_body):
    index = message_body.find("deflate")
    protoc_buff = message_body[index+11:]
    return protoc_buff

def decode_response_envelope(protoc_buff):
    message = POGOProtos_pb2.Networking.Envelopes.ResponseEnvelope()
    message.ParseFromString(protoc_buff)
    return message

def decode_request_envelope(protoc_buff):
    message = POGOProtos_pb2.Networking.Envelopes.RequestEnvelope()
    message.ParseFromString(protoc_buff)
    return message

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
        response_base64 = item.request.getText()
        response = base64.b64decode(response_base64)

        request_body = decode_request_envelope(remove_header(request)) 
        response_body = decode_response_envelope(remove_header(response))

        print "================================================="
        print("Comment: {0}".format(comment))
        print(request_body)
        print "================================================="
        print(response_body)
        print("-------------------------------------------------")

