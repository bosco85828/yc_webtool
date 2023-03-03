'''
support python3 only
'''
# !/usr/local/bin/python
# coding=utf-8
import base64
import hashlib
import time
import json
import requests
from hashlib import sha256
import hmac
from pprint import pprint
import urllib.parse


def canonical_request_method(method, request_uri, request_payload, host):
    signed_headers = 'content-type;host'
    canonical_headers = 'content-type:application/json\nhost:{}\n'.format(host)

    if method == "GET" or method == "DELETE":
        request_payload = ''
    uri = request_uri.split('?')[0]
    if "?" not in request_uri or method == "POST":
        query_string = ""
    else:
        query_string = urllib.parse.unquote(request_uri.split('?')[1])

    hashed_request_payload = hashlib.sha256(request_payload.encode('utf-8')).hexdigest()
    canonical_request = '{}\n{}\n{}\n{}\n{}\n{}'.format(method, uri, query_string, canonical_headers, signed_headers, hashed_request_payload)
    return hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()


def get_authorization_header(access_key, secret_key, timestamp, canonical_request):
    string_to_sign = 'CNC-HMAC-SHA256\n' + str(timestamp) + '\n' + canonical_request
    signature = base64.b16encode(hmac.new(secret_key.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=sha256).digest()).decode()
    authorization = 'CNC-HMAC-SHA256 ' + 'Credential={},'.format(access_key) + ' SignedHeaders=content-type;host,' + ' Signature={}'.format(signature)
    return authorization


def send_request(access_key, secret_key, host, uri, method, post_request_body):
    timestamp = int(time.time())
    canonical_requests = canonical_request_method(method, uri, json.dumps(post_request_body), host)
    authorization_headers = get_authorization_header(access_key, secret_key, timestamp, canonical_requests)
    headers = {
        'x-cnc-auth-method': 'AKSK',
        'x-cnc-accessKey': access_key,
        'x-cnc-timestamp': str(timestamp),
        'Authorization': authorization_headers,
        'Content-Type': 'application/json'
    }
    if method.upper() == 'POST':
        res = requests.post('https://{}'.format(host) + uri, data=json.dumps(post_request_body), headers=headers)
    elif method.upper() == 'GET':
        res = requests.get('https://{}'.format(host) + uri, headers=headers)
    elif method.upper() == 'PUT':
        res = requests.put('https://{}'.format(host) + uri, data=json.dumps(post_request_body), headers=headers)
    elif method.upper() == 'DELETE':
        res = requests.delete('https://{}'.format(host) + uri, headers=headers)
    pprint(res.text)
    return res



if __name__ == '__main__':
    # you can edit ak/sk below
    AccessKey = ''
    SecretKey = ''
    host = 'api.cdnetworks.com'
    http_method = ''
    # if api support get method , please add parameters after uri, exp: test?a=1&b=2&c=3
    uri = ''
    # if api is a post method, please put parameters as dict
    post_request_body = {}
    send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body)
