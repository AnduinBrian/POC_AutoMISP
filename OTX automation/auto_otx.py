from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes
import csv, argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-pid","--pulse", help="pulse id",metavar = "", required=True)
    args = parser.parse_args()
    return args

a = parse_args()
print("[+] Pulling pulse: ", a.pulse)
otx = OTXv2("f401cd929d2450b4d2c90f2165a2958fed37b952ecbf2f42390eba4c29ae4d5a")
ioc = otx.get_pulse_details(a.pulse)
tag = ioc["tags"]
ioc_tag = ""
for i, item in enumerate(tag):
    if i == len(tag) - 1:
        ioc_tag += item
        break
    ioc_tag += item + ";"

file_name = a.pulse + "_export.csv"
with open(file_name,"w", newline = "") as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',')
    for item in ioc["indicators"]:
        csv_writer.writerow([item["indicator"], item["type"], ioc_tag])

print("[+] Done !!")        
