import sys, datetime
import json
import csv
import gzip
import requests
import threading, Queue

_ifttt_server_verify = True
_max_content_bytes = 100000
_max_content_records = 1000
_number_of_threads = 5 

class ifttt:

    def __init__(self, event, api_key):
        self.event = event
        self.api_key = api_key
        self.flushQueue = Queue.Queue(0)
        for x in range(_number_of_threads):
            t = threading.Thread(target=self.batchThread)
            t.daemon = True
            t.start()

    def postDataToIFTTT(self, data):
        self.flushQueue.put(data)
        
    def batchThread(self):
        while True:
            queuedData = self.flushQueue.get()[0]
            print >> sys.stderr, "INFO ifttt send vendor_action=successful %s" % json.dumps(queuedData)
            data = {}
            if 'Value1' in queuedData: data['value1'] = queuedData.get('Value1') 
            if 'Value2' in queuedData: data['value2'] = queuedData.get('Value2')
            if 'Value3' in queuedData: data['value2'] = queuedData.get('Value3')

            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            ifttt_url = ''.join(['https://maker.ifttt.com/trigger/',self.event,'/with/key/',self.api_key,'/'])
            payload_length = sum(len(json.dumps(item)) for item in data)
            r = requests.post(ifttt_url,verify=_ifttt_server_verify,headers=headers,data=json.dumps(data))
            if not r.status_code == requests.codes.ok:
                print >> sys.stderr, ("ERROR ifttt post vendor_action=failed %s" % r.text)
            self.flushQueue.task_done()

    def waitUntilDone(self):
         self.flushQueue.join()
         return

if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        payload = json.loads(sys.stdin.read())
        results_file = payload.get('results_file')
        if not results_file:
            print >> sys.stderr, "FATAL Missing results file"
            sys.exit(1)
        configuration = payload.get('configuration')
        if not configuration:
            print >> sys.stderr, "FATAL Missing configuration"
            sys.exit(1)
    else:
        print >> sys.stderr, "FATAL Unsupported execution mode (expected --execute flag)"
        sys.exit(1)

    event = configuration.get('event')
    api_key = configuration.get('apikey')

    destIFTTT = ifttt(event,api_key)

    try:
        eventContents = csv.DictReader(gzip.open(results_file, 'rb'))

    except Exception, e:
        raise Exception, "%s" % str(e) 

    tableContents = []
    for row in eventContents:
        tableContents.append(row)

    if len(tableContents) == 0:
        print >> sys.stderr, "FATAL Empty Search Results, nothing to sync."
        sys.exit(1)
    try:
        postList = []
        for entry in tableContents:
            if ((len(json.dumps(postList)) + len(json.dumps(entry))) < _max_content_bytes) and (len(postList) + 1 < _max_content_records):
                postList.append(entry)
            else:
                destIFTTT.postDataToIFTTT(postList)
                postList = []
                postList.append(entry)

        destIFTTT.postDataToIFTTT(postList)

    except Exception, e:
        raise Exception, "%s" % str(e)

    destIFTTT.waitUntilDone()
    print >> sys.stderr, "INFO ifttt send vendor_action=successful count=%s" % len(tableContents)


