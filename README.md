# Flask-Rest-API


### Features

Simple Rest API implemented in Flask.

Based on the curse "REST API krok po kroku - Python | Flask | MySQL" by Szymon Wolny

### Environment

   - python 3.8.0
   - pip 20.3.1
   - flask 1.1.2
   - postman 7.36.0


### Installation

##### Ubuntu:

Installation python virtualenv i virtualenvwrapper:

```
$ sudo pip install virtualenv
$ sudo pip install virtualenvwrapper
```

Install postman:
```
$ sudo snap install postman
```

##### Centos:

Installation python virtualenv i virtualenvwrapper:

```
$ yum install -y python-pip
$ pip install -U pip
$ pip install virtualenv
$ pip install virtualenvwrapper
```

Install postman:
```
wget https://dl.pstmn.io/download/latest/linux64 -O postman-linux-x64.tar.gz
sudo tar -xvzf postman-linux-x64.tar.gz -C /opt
sudo ln -s /opt/Postman/Postman /usr/bin/postman
```

### Prepering environment:

```
virtualenv  nip-regon-pesel-validator
source ./nip-regon-pesel-validator/bin/activate
```

```
pip install -r requirements.txt
```

or

```
make deps
```

Deactivating the environment:

```
deactivate 
```


### Run application

Run application more efficiently with makefile. The make utility requires a file, Makefile (or makefile), which defines set of tasks to be executed.

- **Run Flask Rest API**

  `make run`
  
  You can acces on 127.0.0.1:5000


### SQL Flask migrate

Show commands list:
```
flask db 
```
Create new migration repository:
```
flask db init
```
Generate new revision file:
```
flask db migrate
```
Upgrade table to te last version:
```
flask db upgrade
```

# pip install marshmallow

# pip install webargs
