
import time
import requests
import json
import sys
from datetime import datetime


ns_synced = False
ns_firstCall = True
ns_node = '192.168.178.33:8080'

class NodeStatus:
    def get(self):
        global ns_synced, ns_firstCall, ns_node
        try:
            self.r = requests.get('http://' + ns_node + '/info'
                             , timeout=6000)
        except:
            return 'get error: ' + ns_node
        if self.r.ok == True:
            self.__dict__ = json.loads(self.r.text)
            if (ns_firstCall is True) or (ns_synced != self.tangleTime['synced']):
                ns_firstCall = False
                ns_synced = self.tangleTime['synced']
                timestamp = 1545730073
                #dt_object = datetime.fromtimestamp(timestamp)
                timestamp = int(self.tangleTime['time']/1000000000)
                dt_object = datetime.fromtimestamp(timestamp)
                return ns_node + ' : ' + str(dt_object) + '  ' + str(self.tangleTime['synced'])
            else:
                return ''
        else:
            return 'get error: ' + ns_node + ' : ' + str(self.r.status_code) + ' (' + self.r.reason + ')'



if __name__ == '__main__':

    print(len(sys.argv))
    ns = NodeStatus()
    if len(sys.argv) > 1:
        ns_node = sys.argv[1]
    while (True):
       time.sleep(1)
       s = ns.get()
       if len(s) > 0:
          print(s)
