#!/usr/bin/python

import base64
from bs4 import BeautifulSoup

from subprocess import Popen, PIPE

def remove_header(message_body):
    index = message_body.find("deflate")
    protoc_buff = message_body[index+11:]
    return protoc_buff

def decode_protoc_buff(protoc_buff):
    p = Popen(["protoc", "--decode_raw"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    result = p.communicate(protoc_buff)[0]
    print result
    quit()


with open('./request_history', 'r') as input_file:
    xml_doc = input_file.read()
    soup = BeautifulSoup(xml_doc, 'xml')
    items = soup.items.find_all("item")

    for item in items:
        comment = item.comment.getText()
        request_base64 = item.request.getText()
        request = base64.b64decode(request_base64)
        response_base64 = item.request.getText()
        response = base64.b64decode(response_base64)

        request_body = decode_protoc_buff(remove_header(request)) 
