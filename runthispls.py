

import os
import gc
from datetime import datetime
startTime = datetime.now()


print("\n" + "Loaded iftt Data")

os.system('python3 ifttt.py')

print("\n" + "Loaded ap-devices Data")
os.system('python3 safehouse-ap-devices.py')

print("\n" + "Loaded webcam Data")
os.system('python3 webcam-pcap.py')


print("\n" + "Loaded persondetect Data")
os.system('python3 persondetectquery.py')




gc.collect()

#Python 3:
print("Time Took ")
print(datetime.now() - startTime)