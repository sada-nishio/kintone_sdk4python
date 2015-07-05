#!/usr/bin/env python
# -*- coding: utf_8 -*-
'''
from kintone_sdk4python import Kintone

kintone = Kintone()

kintone.set_domain('hw1xj.cybozu.com')
#kintone.set_basic_auth(id, password)
kintone.set_user_auth('sadaya-nishio', 'sadaya-nishio')
#kintone.set_token_auth(token)

#GET
get_record_resp = kintone.get_record(328, 3493)
get_records_resp = kintone.get_records(328, '', ['$id'])

#POST
post_record = {
    'タイトル': {
            'value': 'hoge'
        }
}
post_records = [
    {
        'タイトル': {
            'value': 'hoge'
        }
    },
    {
        'タイトル': {
            'value': 'bar'
        }
    }
]
post_record_resp = kintone.post_record(328, post_record)
post_records_resp = kintone.post_records(328, post_records)

#PUT
put_record = {
    'タイトル': {
        'value': 'hoge'
    }
}
put_records = [
    {
        'id': 3493,
        'record': {
            'タイトル': {
                'value': 'title1'
            }
        }
    },
    {
        'id': 3492,
        'record': {
            'タイトル': {
                'value': 'title2'
            }
        }
    }
]
put_record_resp = kintone.put_record(328, 3493, put_record)
put_records_resp = kintone.put_records(328, put_records)

#DELETE
del_records_resp = kintone.del_records(328, [3490])


print(record_resp)
print(get_records_resp)
print(len(get_records_resp['records']))
print(del_records_resp)
print(post_record_resp)
print(post_records_resp)
print(put_record_resp)
print(put_records_resp)
'''