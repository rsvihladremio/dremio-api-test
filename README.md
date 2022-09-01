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
