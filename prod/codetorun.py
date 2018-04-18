
# Run scripts

import os
import gc
from datetime import datetime
startTime = datetime.now()


os.system('python3 ifttt.py')
print("\n" + "Loaded iftt Data")

os.system('python3 safehouse-ap-devices.py')
print("\n" + "Loaded ap-devices Data")

os.system('python3 webcam-pcap.py')
print("\n" + "Loaded webcam Data")

os.system('python3 persondetectquery.py')
print("\n" + "Loaded persondetect Data")

os.system('python3 gammarf.py')
print("\n" + "Loaded gamma Data")

os.system('python3 combine-sequence-anomaly.py')
print("\n" + "Transformed Data")



os.system('Rscript anomalyDetector.R')
print("\n" + "Algo Performed")

os.system('python3 algosent.py')
print("\n" + "Elastic Search Send Logic")

gc.collect()

#Python 3:
print("Time Took ")
print(datetime.now() - startTime)


