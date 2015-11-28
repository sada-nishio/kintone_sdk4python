#!/usr/bin/env python
# -*- coding: utf_8 -*-

try:
    import os
    import sys
    import base64
    import urllib
    import json
    import requests as req
except:
    print("Error: can't import library")

class Kintone:
    '''
    kintone SDK for Python is kintone REST API Library.

    '''
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
    def make_headers(self, method, is_json=True):
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
            if (is_json):
                headers['Content-Type'] = 'application/json'
        return headers

    ##adding URL parameters.
    def make_inquiry(self, params):
        inquiry_string = urllib.parse.urlencode(params)
        return inquiry_string

    #Execution REST API
    ##Getting Record.
    def get_record(self, app_id, record_id, guest_space_id=''):
        method = 'GET'
        params = {
            'app': app_id,
            'id': record_id
        }
        try:
            url = self.make_url('record', guest_space_id) + self.make_inquiry(params)
            headers_obj = self.make_headers(method)
        except:
            err = "Error: can't make URL or request headers."
            return err
        try:
            resp = req.request(method, url, headers=headers_obj)
            return json.loads(resp.text)
        except:
            err = 'Error: failed sending request.'
            #print(err)
            return err

    ##Getting Records by query.
    def get_records(self, app_id, query='', fields=[], all_records=False, guest_space_id=''):
        method = 'GET'
        params = {
            'app': app_id,
            'totalCount': True
        }
        try:
            headers_obj = self.make_headers(method)
        except:
            err = "Error: can't make request headers."
            return err
        if len(fields) > 100:
            err = 'Error: fields is needed less than 100 items.'
            return err
        if (fields):
            i = 0
            for field in fields:
                params['fields' + '[' + str(i) + ']'] = field
                i += 1
        #All records or not
        limit = 500
        if (all_records == False):
            if(query):
                params['query'] = query + ' limit ' + str(limit)
            else:
                params['query'] = 'limit ' + str(limit)
            try:
                url = self.make_url('records', guest_space_id) + self.make_inquiry(params)
            except:
                err = 'Error: failed sending request.'
                return err
            try:
                resp = req.request(method, url, headers=headers_obj)
                return json.loads(resp.text)
            except:
                err = 'Error: Failed Sending Request.'
                return err
        else:
            response = {
                'records': []
            }
            offset = 0
            while True:
                if(query):
                    params['query'] = query + ' limit ' + str(limit) + ' offset ' + str(offset)
                else:
                    params['query'] =  'limit ' + str(limit) + ' offset ' + str(offset)
                try:
                    url = self.make_url('records', guest_space_id) + self.make_inquiry(params)
                except:
                    err = "Error: can't make URL."
                    return err
                try:
                    resp = req.request(method, url, headers=headers_obj)
                    tmp_resp = json.loads(resp.text)
                    #Error:
                    if ('errors' in tmp_resp):
                        return tmp_resp
                    #Success:
                    for record in tmp_resp['records']:
                        response['records'].append(record)
                    if len(tmp_resp['records']) < limit:
                        break
                    else:
                        offset += limit
                except:
                    err = 'Error: failed sending request.'
                    return err
            return response

    ##Deleting Records
    def delete_records(self, app_id, record_ids, guest_space_id=''):
        method = 'DELETE'
        params = {
            'app': app_id
        }
        if (len(record_ids) > 100):
            err = 'Error: record_ids is needed less than 100 items.'
            return err
        if (record_ids):
            i = 0
            for id in record_ids:
                params['ids' + '[' + str(i) + ']'] = id
                i += 1
        try:
            url = self.make_url('records', guest_space_id) + self.make_inquiry(params)
            headers_obj = self.make_headers(method)
        except:
            err = "Error: can't make URL or request headers."
            return err
        try:
            resp = req.request(method, url, headers=headers_obj)
            return json.loads(resp.text)
        except:
            err = 'Error: failed sending request.'
            return err

    ##Post Record.
    def post_record(self, app_id, record={}, guest_space_id=''):
        method = 'POST'
        params = {
            'app': app_id
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
            resp = req.request(method, url, data=json.dumps(params), headers=headers_obj)
            response = json.loads(resp.text)
            return response
        except:
            err = 'Error: failed sending request.'
            return err

    ##Post Records.
    def post_records(self, app_id, records, guest_space_id=''):
        if (len(records) > 100):
            err = 'Error: records is needed less than 100 items.'
            return err
        method = 'POST'
        params = {
            'app': app_id,
            'records': records
        }
        try:
            url = self.make_url('records', guest_space_id)
            headers_obj = self.make_headers(method)
        except:
            err = "Error: can't make URL or request headers."
            return err
        try:
            resp = req.request(method, url, data=json.dumps(params), headers=headers_obj)
            response = json.loads(resp.text)
            return response
        except:
            err = 'Error: failed sending request.'
            return err

    ##Put Record.
    def put_record(self, app_id, record_id, record={}, guest_space_id=''):
        method = 'PUT'
        params = {
            'app': app_id,
            'id': record_id
        }
        if (record):
            params['record'] = record
        try:
            url = self.make_url('record', guest_space_id)
            headers_obj = self.make_headers(method)
        except:
            err = "Error: can't make URL or request headers."
            return err
        try:
            resp = req.request(method, url, data=json.dumps(params), headers=headers_obj)
            response = json.loads(resp.text)
            return response
        except:
            err = 'Error: failed sending request.'
            return err

    ##Post Records.
    def put_records(self, app_id, records, guest_space_id=''):
        method = 'PUT'
        params = {
            'app': app_id,
            'records': records
        }
        if (len(records) > 100):
            err = 'Error: records is needed less than 100 items.'
            return err
        try:
            url = self.make_url('records', guest_space_id)
            headers_obj = self.make_headers(method)
        except:
            err = "Error: can't make URL or request headers."
            return err
        try:
            resp = req.request(method, url, data=json.dumps(params), headers=headers_obj)
            response = json.loads(resp.text)
            return response
        except:
            err = 'Error: failed sending request.'
            return err

    ##Download File
    def download_file(self, file_key=''):
        method = 'GET'
        if (not file_key):
            return 'fileKey is needed.'
        params = {
            'fileKey': file_key
        }
        try:
            url = self.make_url('file') + self.make_inquiry(params)
            headers_obj = self.make_headers(method)
        except:
            err = "Error: can't make URL or request headers."
            return err
        try:
            print(url)
            resp = req.request(method, url, headers=headers_obj)
            return resp.content # this is bytes.
        except:
            err = 'Error: failed sending request.'
            return err

    ##Upload File
    def upload_file(self, file_name, binary):
        method = 'POST'
        try:
            url = self.make_url('file')
            headers_obj = self.make_headers(method, False)
        except:
            err = "Error: can't make URL or request headers."
            return err
        try:
            files = {'file': (file_name, binary, 'application/octet-stream')}
            resp = req.request(method, url, files=files, headers=headers_obj)
            return json.loads(resp.text)
        except:
            err = 'Error: failed sending request.'
            return err
