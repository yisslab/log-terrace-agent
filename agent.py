import subprocess
import select
import sys
import json

import requests

device_id = sys.argv[1]
log_file = sys.argv[2]
server_url = sys.argv[3] + '/log'

f = subprocess.Popen(['tail', '-F', log_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)

while True:
    if p.poll(1):
        line = f.stdout.readline()
        log_message = {
            "device_id": "%s" % device_id,
            "msg": "%s" % line,
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        res = requests.post(server_url, headers=headers, data=json.dumps(log_message))
