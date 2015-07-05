# kintone SDK for Python
kintone SDK for Python

##Requrements
Python 4.3 or Later
pip

##Dependency
* [httplib2](https://github.com/jcgregorio/httplib2)

##Installation
```{.bash}
#install
$ sudo pip install -U git+https://github.com/sada-nishio/kintone_sdk4python.git
#uninstall
$ sudo pip uninstall kintone_sdk4python
```

##Usage
```{.python}
#make class and set domain, authentication(user auth or api-token auth)
kintone = Kintone()
kintone.set_domain('example.cybozu.com')
kintone.set_user_auth('login_name', 'password')
kintone.set_token_auth('api-token')

#get record
kintone.get_record(app_num, record_id, guest_space_id)

#get records
kintone.get_records(app_num, query='', fields=[], all_records=False, guest_space_id='')

#post record
post_record(app_num, record={}, guest_space_id='')

#post records
post_records(app_num, records, guest_space_id='')

#put record
put_record(app_num, id, record={}, guest_space_id='')

#put records
put_records(app, records, guest_space_id='')

#delete records
del_records(app_num, ids, guest_space_id='')
```

##License
MIT License