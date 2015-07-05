#!/usr/bin/env python
# -*- coding: utf_8 -*-

import sys
from kintone_sdk4python import Kintone

kintone = Kintone()

kintone.set_domain('example.cybozu.com')
kintone.set_basic_auth('id', 'password')
kintone.set_user_auth('login_name', 'password')
kintone.set_token_auth('token')

#GET
get_record_resp = kintone.get_record(10, 1)
get_records_resp = kintone.get_records(10, 'レコード番号 > 10', ['$id', '作成日時'])
get_all_records_resp = kintone.get_records(10, '', ['$id', '作成日時'], True)

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
post_record_resp = kintone.post_record(10, post_record)
post_records_resp = kintone.post_records(10, post_records)

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
put_record_resp = kintone.put_record(10, 1, put_record)
put_records_resp = kintone.put_records(10, put_records)

#DELETE
del_records_resp = kintone.del_records(10, [1, 2, 3])

print(get_record_resp)
print(get_records_resp)
print(len(get_records_resp['records']))
print(get_all_records_resp)
print(len(get_all_records_resp['records']))
print(post_record_resp)
print(post_records_resp)
print(put_record_resp)
print(put_records_resp)
print(del_records_resp)