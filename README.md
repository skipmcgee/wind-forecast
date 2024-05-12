# wind-forecast
wind forecast data 

### if first run, install the requirements:
1) follow the os-specific install instructions at: https://pypi.org/project/mysqlclient/
2) `python3 -m venv venv`
3) `source venv/bin/activate` or `venv\Scripts\activate` on Windows.
4) `pip install --upgrade pip setuptools wheel`
5) `pip install -r requirements.txt`

### then create your database connection file:
- open database/.env
- add the following customized variables:
    ```
    340DBHOST='mydbhost'
    340DBUSER='myusername'
    340DBPW='mypw'
    340DB='mydb'
    ```

### make sure your network or local db is set up:
1) confirm database name, user, pass
2) `source DDL.sql` to create tables and data

### To actually run the app:
1) `source venv/bin/activate` or if on Windows `venv\Scripts\activate`
2) `python3 app.py`