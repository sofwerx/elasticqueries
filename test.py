import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile

import zipfile
from datetime import datetime
import json
import requests
import os
from requests.auth import HTTPBasicAuth

from collections import defaultdict
from io import StringIO

# import ujson as json
import pandas as pd

import time
import sys
import cv2
#

columns = ['DateTime', 'Status']
index = [0]


timenow = datetime.utcnow()
df_ = pd.DataFrame(index=index, columns=columns)

df_.loc[0, 'DateTime'] = timenow
df_.loc[0, 'Status'] = 1


jn = df_.to_json(orient='records', lines=True)

jn1 = json.loads(jn)
print(jn)
#
    #
url = 'https://elasticsearch.blueteam.devwerx.org:443/sfalgo/_doc'
username = 'elastic'
password = 'taiko7Ei'
headers = {'Content-Type': 'application/json', 'X-HTTP-Method-Overide': 'PUT', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=json.dumps(jn1), headers=headers, auth=HTTPBasicAuth(username, password))
