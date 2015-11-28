#!/usr/bin/env python
# -*- coding: utf_8 -*-

import sys
import os
from kintone_sdk4python import Kintone

kintone = Kintone()

#Authentication
kintone.set_domain('example.cybozu.com')            #required
kintone.set_basic_auth('id', 'password')
kintone.set_user_auth('login_name', 'password')
kintone.set_token_auth('token')

#GET
app_id = 10
record_id = 1
##Single Record
get_record_resp = kintone.get_record(app_id, record_id)
print(get_record_resp)
##Multi Records (~500 records)
query = 'レコード番号 > 10'
fields = ['$id', '作成日時']
get_records_resp = kintone.get_records(app_id, query, fields)
print(get_records_resp)
##All Records
get_all_records_resp = kintone.get_records(app_id, query, fields, all_records=True)
print(get_all_records_resp)

#POST
post_record = {
    'title': {
        'value': 'title1'
    }
}
post_records = [
    {
        'title': {
            'value': 'title1'
        }
    },
    {
        'title': {
            'value': 'title2'
        }
    }
]
##Single Record
post_record_resp = kintone.post_record(app_id, post_record)
print(post_record_resp)
##Multi Records (~100 records)
post_records_resp = kintone.post_records(app_id, post_records)
print(post_records_resp)

#PUT
put_record = {
    'title': {
        'value': 'change_title'
    }
}
put_records = [
    {
        'id': 1,
        'record': {
            'title': {
                'value': 'change_title1'
            }
        }
    },
    {
        'id': 2,
        'record': {
            'title': {
                'value': 'change_title1'
            }
        }
    }
]
##Single Record
record_id = 1
put_record_resp = kintone.put_record(app_id, 1, put_record)
print(put_record_resp)
##Multi Records
put_records_resp = kintone.put_records(app_id, put_records)
print(put_records_resp)

#DELETE
record_ids = [1, 2, 3]
del_records_resp = kintone.delete_records(app_id, record_ids)
print(del_records_resp)

#Download File
file_path = './sample.png'
file_key = '20151128..........'
binary = kintone.download_file(file_key)
with open(file_path, 'rb') as f:
    f.write(binary)

#Upload File
file_name = 'sample.png'
upload_file_resp = kintone.upload_file(file_name, binary)
print(upload_file_resp)
