#!/usr/bin/env python
# -*- coding: utf_8 -*-
from .kintone_sdk import Kintone

__author__ = 'sadaya-nishio'
__version__ = '0.0.1'
__license__ = 'MIT License'



kintone = Kintone()
kintone.set_domain('hw1xj.cybozu.com')
kintone.set_user_auth('sadaya-nishio', 'sadaya-nishio')

#get_record_resp = kintone.get_record(328, 3485)
#get_records_resp = kintone.get_records(328, '', ['$id'])
#del_records_resp = kintone.del_records(328, [3490])
#post_record_resp = kintone.post_record(328)
'''POST
records = [
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
post_records_resp = kintone.post_records(328, records)
'''
'''PUT
record = {
    'タイトル': {
        'value': 'hoge'
    }
}
put_record_resp = kintone.put_record(328, 3493, record)
'''
records = [
    {
        'id': 3493,
        'record': {
            'タイトル': {
                'value': 'title'
            }
        }
    },
    {
        'id': 3492,
        'record': {
            'タイトル': {
                'value': 'title'
            }
        }
    }
]
put_records_resp = kintone.put_records(328, records)


#print(record_resp)
#print(get_records_resp)
#print(len(get_records_resp['records']))
#print(del_records_resp)
#print(post_record_resp)
#print(post_records_resp)
#print(put_record_resp)
print(put_records_resp)