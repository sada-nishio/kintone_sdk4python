# kintone SDK for Python
kintone SDK for Python is kintone REST API Library.

##Version
* 1.1.0

##Requrements
* Python 3.4 or Later

##Dependency
* [requests](https://github.com/kennethreitz/requests/)

##Installation
```{.bash}
#install
$ sudo pip install -U git+https://github.com/sada-nishio/kintone_sdk4python.git
#uninstall
$ sudo pip uninstall kintone-SDK-for-Python
```

##Usage
```{.python}
from kintone_sdk4python import Kintone

#make class and set domain, authentication(user auth or api-token auth)
kintone = Kintone()
kintone.set_domain('example.cybozu.com')
kintone.set_basic_auth('id', 'password')
kintone.set_user_auth('login_name', 'password')
kintone.set_token_auth('api-token')

#get record
kintone.get_record(app_id, record_id, guest_space_id)

#get records
kintone.get_records(app_id, query='', fields=[], all_records=False, guest_space_id='')

#post record
kintone.post_record(app_id, record={}, guest_space_id='')

#post records
kintone.post_records(app_id, records, guest_space_id='')

#put record
kintone.put_record(app_id, record_id, record={}, guest_space_id='')

#put records
kintone.put_records(app, records, guest_space_id='')

#delete records
kintone.delete_records(app_id, record_ids, guest_space_id='')

#download file
kintone.download_file(file_key='')

#upload file
kintone.upload_file(file_name, binary)
```

##License
MIT License
