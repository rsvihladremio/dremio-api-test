import json
import requests
import argparse
import time


def api_get(endpoint, dremio_server, headers):
  url = '{server}/api/v3/{endpoint}'.format(server=dremio_server, endpoint=endpoint)
  #print(url)
  return json.loads(requests.get(url, headers=headers).text)

def api_post(endpoint, dremio_server, headers, body=None):
  url = '{server}/api/v3/{endpoint}'.format(server=dremio_server, endpoint=endpoint)
  #print(url)
  #print(headers)
  #print(body)
  text = requests.post(url, headers=headers, data=json.dumps(body)).text

  # a post may return no data
  if (text):
    return json.loads(text)
  else:
    return None

def api_put(endpoint, dremio_server, headers, body=None):
  return requests.put('{server}/api/v3/{endpoint}'.format(server=dremio_server, endpoint=endpoint), headers=headers, data=json.dumps(body)).text

def api_delete(endpoint, dremio_server, headers):
  return requests.delete('{server}/api/v3/{endpoint}'.format(server=dremio_server, endpoint=endpoint), headers=headers)

def query_sql(query, dremio_server, headers):
  query_response = api_post('sql', dremio_server, headers, body={'sql': query})
  if query_response is None:
      raise ValueError("response is empty and therefore the query failed")
  if 'id' not in query_response:
      raise ValueError("response '%s' is missing key 'id' cannot query" % query_response)
  jobid = query_response['id']
  return jobid

def login(username, password, dremio_server):
  # we login using the old api for now
  login_data = {'userName': username, 'password': password}
  response = requests.post(dremio_server + '/apiv2/login', headers={'content-type':'application/json'}, data=json.dumps(login_data))
  data = json.loads(response.text)
  if 'token' not in data:
      raise ValueError("response '%s' is missing key 'token' cannot login" % data)
  # retrieve the login token
  token = data['token']
  return {'content-type':'application/json', 'authorization':'_dremio{auth_token}'.format(auth_token=token)}

def run(args):
    username = args.username
    password = args.password
    dremio_server = args.dremio
    headers = login(username, password, dremio_server)
    jobid = query_sql(args.query[0], dremio_server, headers)
    while True:
        try:
            time.sleep(args.pollfreq/1000)
            job_status = api_get('job/%s' % jobid, dremio_server, headers)
            print("job status is %s" % job_status)
        except KeyboardInterrupt:
            job_status = api_get('job/%s' % jobid, dremio_server, headers)
            print("exiting with final job status of %s for job id %s" % (job_status, jobid))
            exit(0)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--username', help='username to log into dremio')
    parser.add_argument('--password', help='password to log into dremio')
    parser.add_argument('query', nargs='*', help='query to send to the server for testing')
    parser.add_argument('--dremio',  nargs='?', default='http://localhost:9047', help='url for the dremio server')
    parser.add_argument('--pollfreq', nargs='?', default=10, type=int, help='poll job status every x milliseconds')

    args = parser.parse_args()
    run(args)
