# to run

1. make sure you have python 3.x
2. run the following:
 ```sh
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python cli.py --username myuser --password 'mypassword' "select * from \"localhost mysql\".tester.records"
```
3. ctl+c to exit

# Help

cli.py -h       
usage: cli.py [-h] [--username USERNAME] [--password PASSWORD] [--dremio [DREMIO]] [query ...]

Process some integers.

positional arguments:
  query                query to send to the server for testing

optional arguments:
  -h, --help           show this help message and exit
  --username USERNAME  username to log into dremio
  --password PASSWORD  password to log into dremio
  --dremio [DREMIO]    url for the dremio server
