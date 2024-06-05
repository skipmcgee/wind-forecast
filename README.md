# wind-forecast
application for wind forecast and wind reading data analysis

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

### (optional) add your sensor api keys:
- open app/.env
- add the following customized variables:
    ```
    HOLFUY_STATION='1151'
    HOLFUY_TOKEN='mytoken'
    ```

### make sure your network or local db is set up:
1) confirm database name, user, pass
2) `source DDL.sql` to create tables and data

### To actually run the app:
1) `source venv/bin/activate` or if on Windows `venv\Scripts\activate`
2) `python3 app.py`

### Syntax to run via Gunicorn:
`gunicorn --config gunicorn.py wsgi:app`

## Code referenced for this project (accessed repeatedly April-June 2024):
- https://open-meteo.com/en/docs/ecmwf-api
- https://open-meteo.com/en/docs/gfs-api
- https://api.holfuy.com/live/ 
- https://github.com/osu-cs340-ecampus/flask-starter-app/
- https://stackoverflow.com/questions/207981/how-to-enable-mysql-client-auto-re-connect-with-mysqldb/982873#982873
