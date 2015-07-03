#!/usr/bin/env python
# -*- coding: utf_8 -*-

import sys
import base64
import urllib
import httplib2
import json

class Kintone:
    """
    kintone SDK for Python
    @user_auth
    @token_auth
    @user_basic_auth

    """
    #initialize
    def __init__(self):
        self.user_auth = {}
        self.token_auth = {}
        self.domain = ''
        self.basic_auth = {}

    #Method for Authentication
    ##setting User Information using for Authentication.
    def set_user_auth(self, name, password):
        self.user_auth = {
            'login_name': name,
            'password': password
        }

    ##setting API-Token Auth information.
    def set_token_auth(self, token):
        self.token_auth = {
            'token': token
        }

    ##setting Basic Auth information.
    def set_basic_auth(self, name, password):
        self.basic_auth = {
            'name': name,
            'password': password
        }

    #Request Parameters
    ##setting domain name
    def set_domain(self, domain_name):
        self.domain = domain_name

    ##setting URL by domain and guest_space_id.
    def make_url(self, api, guest_space_id=''):
        url = ''
        if (not guest_space_id):
            url = 'https://' + self.domain + '/k/v1/' + api + '.json?'
        else:
            url = 'https://' + self.domain + '/k/guest/' + str(guest_space_id) + '/v1/' + api + '.json?'
        return url

    ##setting headers
    def make_headers(self, method):
        headers = {
            'Host': self.domain + ':443'
        }
        #basic auth
        if (self.basic_auth):
            basic_pass = self.basic_auth['name'] + ':' + self.basic_auth['password']
            headers['Authorization'] = 'Basic ' + base64.b64encode(basic_pass.encode('utf-8'))
        #user auth
        if (self.user_auth):
            user_pass = self.user_auth['login_name'] + ':' + self.user_auth['password']
            headers['X-Cybozu-Authorization'] = base64.b64encode(user_pass.encode('utf-8'))
        #API-Token auth
        if (self.token_auth):
            headers['X-Cybozu-API-Token'] = self.token_auth['token']
        #Content-Type
        if (method == 'POST' or method == 'PUT'):
            headers['Content-Type'] = 'application/json'
        return headers

    ##adding URL parameters.
    def make_inquiry(self, params):
        inquiry_string = urllib.parse.urlencode(params)
        return inquiry_string

    #Execution REST API
    ##Getting Record.
    def get_record(self, app, id, guest_space_id=''):
        method = 'GET'
        params = {
            'app': app,
            'id': id
        }
        url = self.make_url('record', guest_space_id) + self.make_inquiry(params)
        headers_obj = self.make_headers(method)
        http_client = httplib2.Http()
        (resp_headers, content) = http_client.request(url, method, headers=headers_obj)
        #for debug
        #print(resp_headers)
        return json.loads(content.decode('utf-8'))

    ##Getting Records by query.
    def get_records(self, app, query='', fields=[], totalCount=False, guest_space_id=''):
        method = 'GET'
        params = {
            'app': app
        }
        if (query):
            params['query'] = query
        if (fields):
            i = 0
            for field in fields:
                params['fields' + '[' + str(i) + ']'] = field
                i += 1
        if (totalCount):
            params['totalCount'] = totalCount
        url = self.make_url('records', guest_space_id) + self.make_inquiry(params)
        print(url)
        headers_obj = self.make_headers(method)
        http_client = httplib2.Http()
        (resp_headers, content) = http_client.request(url, method, headers=headers_obj)
        #for debug
        #print(resp_headers)
        return json.loads(content.decode('utf-8'))

