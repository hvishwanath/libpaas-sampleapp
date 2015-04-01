import random
import time
import json
import signal
import os
from wsgiref.simple_server import make_server

def _sleep_handler(signum, frame):
    print "SIGINT Received. Stopping CAF"
    raise KeyboardInterrupt

def _stop_handler(signum, frame):
    print "SIGTERM Received. Stopping CAF"
    raise KeyboardInterrupt


signal.signal(signal.SIGTERM, _stop_handler)
signal.signal(signal.SIGINT, _sleep_handler)


PORT = int(os.environ.get('PORT', 9000))
HOST = os.environ.get('HOST', '0.0.0.0')

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults

import re

def get_system_memory():
    meminfo = open('/proc/meminfo').read()
    matched = re.search(r'^MemTotal:\s+(\d+)', meminfo)
    if matched:
        mem_total_mb = str(int(matched.groups()[0]) / 1024) + " MB"
    else:
        mem_total_mb = "UNKNOWN"
    return mem_total_mb


def simple_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    d = dict()
    d["sensors"] = {}
    d["sensors"]["shopfloor_temp_1"] = {"status" : "OK", "value": str(random.randrange(20, 30)), "unit" : "degree c"}
    d["sensors"]["exit_valve_pressure_1"] = {"status" : "OK", "value": str(random.randrange(40, 50)), "unit" : "pascals"}
    d["sensors"]["new_sensor"] = {"status" : "OK", "value": str(random.randrange(40, 50)), "unit" : "pascals"}
    start_response(status, headers)
    ret = json.dumps(d)
    return ret

print "Serving on port %s:%s" % (HOST, str(PORT))
httpd = make_server(HOST, PORT, simple_app)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.shutdown()
