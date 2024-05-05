# wind-forecast
wind forecast data 

### if first run, install the requirements:
1) follow the os-specific install instructions at: https://pypi.org/project/mysqlclient/
2) `python3 -m venv venv`
3) `source venv/bin/activate`
4) `pip install --upgrade pip setuptools wheel`
5) `pip install -r requirements.txt`

### then create your database connection file:
- open database/.env
- add the following customized variables:
    ```340DBHOST='mydbhost'
    340DBUSER='myusername'
    340DBPW='mypw'
    340DB='mydb'```

### if not first run::
1) `source venv/bin/activate`
2) `python3 app.py`