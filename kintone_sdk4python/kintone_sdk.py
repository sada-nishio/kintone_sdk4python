#!/usr/bin/env python
# -*- coding: utf_8 -*-

try:
    import base64
    import urllib
    import httplib2
    import json
except:
    print("Error: can't import library")

class Kintone:
    """
    kintone SDK for Python

    """
    #initialize
    def __init__(self):
        self.user_auth = {}
        self.token_auth = {}
        self.domain = ''
        self.basic_auth = {}

    #Request Parameters
    ##setting domain name
    def set_domain(self, domain_name):
        self.domain = domain_name

    ##setting Basic Auth information.
    def set_basic_auth(self, id, password):
        self.basic_auth = {
            'id': id,
            'password': password
        }

    #Method for Authentication
    ##setting User Information using for Authentication.
    def set_user_auth(self, login_name, password):
        self.user_auth = {
            'login_name': login_name,
            'password': password
        }

    ##setting API-Token Auth information.
    def set_token_auth(self, token):
        self.token_auth = {
            'token': token
        }

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
            basic_pass = self.basic_auth['id'] + ':' + self.basic_auth['password']
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
        try:
            url = self.make_url('record', guest_space_id) + self.make_inquiry(params)
            headers_obj = self.make_headers(method)
        except:
            err = "Error: can't make URL or request headers."
            #print(err)
            return err
        try:
            http_client = httplib2.Http()
            (resp_headers, content) = http_client.request(url, method, headers=headers_obj)
            response = json.loads(content.decode('utf-8'))
            #for debug
            #print(resp_headers)
            return response
        except:
            err = "Error: failed sending request."
            #print(err)
            return err

    ##Getting Records by query.
    def get_records(self, app, query='', fields=[], all_records=False, guest_space_id=''):
        if len(fields) > 100:
            err = 'Error: fields is needed less than 100 items.'
            #print(err)
            return err
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

        if (all_records == False):
            params['query'] = query
            try:
                url = self.make_url('records', guest_space_id) + self.make_inquiry(params)
                headers_obj = self.make_headers(method)
                #for debug
                #print(url)
            except:
                err = "Error: failed sending request."
                #print(err)
                return err
            try:
                http_client = httplib2.Http()
                (resp_headers, content) = http_client.request(url, method, headers=headers_obj)
                return json.loads(content.decode('utf-8'))
            except:
                err = "Error: can't make URL or request headers."
                #print(err)
                return err
        else:
            response = {
                'records': []
            }
            try:
                headers_obj = self.make_headers(method)
            except:
                err = "Error: can't make request headers."
                #print(err)
                return err
            offset = 0
            while True:
                params['query'] = query + ' offset ' + str(offset)
                try:
                    url = self.make_url('records', guest_space_id) + self.make_inquiry(params)
                except:
                    err = "Error: can't make URL."
                    #print(err)
                    return err
                #for debug
                #print(url)
                try:
                    (resp_headers, content) = http_client.request(url, method, headers=headers_obj)
                    tmp_resp = json.loads(content.decode('utf-8'))
                    #Error:
                    if (tmp_resp['errors']):
                        return tmp_resp
                    #Success:
                    for record in tmp_resp['records']:
                        response['records'].append(record)
                    #for debug
                    #print(resp_headers)
                    if len(tmp_resp['records']) < 100:
                        break
                    else:
                        offset += 100
                except:
                    err = "Error: failed sending request."
                    #print(err)
                    return err
            return response

    ##Deleting Records
    def del_records(self, app, ids, guest_space_id=''):
        if (len(ids) > 100):
            err = 'Error: ids is needed less than 100 items.'
            #print(err)
            return err
        method = 'DELETE'
        params = {
            'app': app
        }
        try:
            url = self.make_url('records', guest_space_id) + self.make_inquiry(params)
            headers_obj = self.make_headers(method)
        except:
            err = "Error: can't make URL or request headers."
            #print(err)
            return err
        try:
            http_client = httplib2.Http()
            (resp_headers, content) = http_client.request(url, method, headers=headers_obj)
            #for debug
            #print(resp_headers)
            return json.loads(content.decode('utf-8'))
        except:
            err = "Error: failed sending request."
            #print(err)
            return err

    ##Post Record.
    def post_record(self, app, record={}, guest_space_id=''):
        method = 'POST'
        params = {
            'app': app
        }
        if (record):
            params['record'] = record
        try:
            url = self.make_url('record', guest_space_id)
            headers_obj = self.make_headers(method)
        except:
            err = "Error: can't make URL or request headers."
            #print(err)
            return err
        try:
            http_client = httplib2.Http()
            (resp_headers, content) = http_client.request(url, method, body=json.dumps(params), headers=headers_obj)
            response = json.loads(content.decode('utf-8'))
            #for debug
            #print(resp_headers)
            return response
        except:
            err = "Error: failed sending request."
            #print(err)
            return err

    ##Post Records.
    def post_records(self, app, records, guest_space_id=''):
        if (len(records) > 100):
            err = 'Error: records is needed less than 100 items.'
            #print(err)
            return err
        method = 'POST'
        params = {
            'app': app,
            'records': records
        }
        try:
            url = self.make_url('records', guest_space_id)
            headers_obj = self.make_headers(method)
        except:
            err = "Error: can't make URL or request headers."
            #print(err)
            return err
        try:
            http_client = httplib2.Http()
            (resp_headers, content) = http_client.request(url, method, body=json.dumps(params), headers=headers_obj)
            response = json.loads(content.decode('utf-8'))
            #for debug
            #print(resp_headers)
            return response
        except:
            err = "Error: failed sending request."
            #print(err)
            return err

    ##Put Record.
    def put_record(self, app, id, record={}, guest_space_id=''):
        method = 'PUT'
        params = {
            'app': app,
            'id': id
        }
        if (record):
            params['record'] = record
        try:
            url = self.make_url('record', guest_space_id)
            headers_obj = self.make_headers(method)
        except:
            err = "Error: can't make URL or request headers."
            #print(err)
            return err
        try:
            http_client = httplib2.Http()
            (resp_headers, content) = http_client.request(url, method, body=json.dumps(params), headers=headers_obj)
            response = json.loads(content.decode('utf-8'))
            #for debug
            #print(resp_headers)
            return response
        except:
            err = "Error: failed sending request."
            #print(err)
            return err

    ##Post Records.
    def put_records(self, app, records, guest_space_id=''):
        if (len(records) > 100):
            err = 'Error: records is needed less than 100 items.'
            #print(err)
            return err
        method = 'PUT'
        params = {
            'app': app,
            'records': records
        }
        try:
            url = self.make_url('records', guest_space_id)
            headers_obj = self.make_headers(method)
        except:
            err = "Error: can't make URL or request headers."
            #print(err)
            return err
        try:
            http_client = httplib2.Http()
            (resp_headers, content) = http_client.request(url, method, body=json.dumps(params), headers=headers_obj)
            response = json.loads(content.decode('utf-8'))
            #for debug
            #print(resp_headers)
            return response
        except:
            err = "Error: failed sending request."
            #print(err)
            return err
