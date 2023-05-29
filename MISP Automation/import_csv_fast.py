from pymisp import ExpandedPyMISP, MISPEvent, MISPAttribute
import os, csv, urllib3

# disable warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

IOC_TYPE = {
    "URL": "url",
    "hostname" : "hostname",
    "domain" : "domain"
}

CATEGORY = {
    "URL" : "Network activity",
    "hostname" : "Network activity",
    "domain" : "Network activity"
}

class MISP:
    def __init__(self, url, key):
        self.url = url
        self.key = key
        self.api = ExpandedPyMISP(self.url, self.key, False, "json", proxies=None)

    def create_event(self, MISP_Event):
        event = self.api.add_event(MISP_Event, pythonify=True)
        print("[+] Created and Publish Event: ", event.id)
        return event
    
    def add_attribute_event(self, event_id, MISP_Attr):
        r = self.api.add_attribute(event_id, MISP_Attr)
        if "errors" in r:
            print("[!] Fail to add attribute for event ", event_id)
        else:
            print("[+] Added attribute for event ", event_id)
            return r
    def delete_event(self, event_id):
        self.api.delete_event(event_id)
        print("[+] Deleted Event: ", event_id)
    
    def publish_event(self, event_id):
        self.api.publish(event_id)
        print("[+] Published Event: ", event_id)

def Get_Config(file_path):
    bIs_Existing = os.path.exists(file_path)
    if bIs_Existing == False:
        print("[!] Error: config file not found !!")
        exit(ERR_PATH_NOT_FOUND)
    else:
        temp_arr = []
        with open(file_path,"r") as file:
            for line in file:
                temp = line.strip().split("=")
                for i in temp:
                    temp_arr.append(i.strip())
        it = iter(temp_arr)
        config = dict(zip(it, it))
        for i in config:
            if config[i] == "":
                print("[!] Found null setting !!")
                exit(ERR_CONFIG)
        return config

def create_event_obj(info, tags = [], distrib=0, threat=1, analysis=0):
    event = MISPEvent()
    event.distribution = distrib
    event.threat_level_id = threat
    event.analysis = analysis
    event.info = info
    for tag in tags:
        event.add_tag(tag)
    return event

def create_attr_obj(value, category, att_type, comment, to_ids, tags):
    misp_attribute = MISPAttribute()
    misp_attribute.value = str(value)
    misp_attribute.category = str(category)
    misp_attribute.type = str(att_type)
    misp_attribute.comment = str(comment)
    misp_attribute.to_ids = str(to_ids)
    for tag in tags:
        misp_attribute.add_tag(tag)
    return misp_attribute

def read_csv_file(file_path):
    ioc = []
    with open(file_path, "r") as csv_file:
        reader = csv.reader(csv_file, delimiter = ",")
        for i, line in enumerate(reader):
            temp = []
            for item in line:
                temp.append(item)
            ioc.append(temp)
    return ioc

strConfig_File_Path = os.getcwd() + "/config.cfg"
dictConfig = Get_Config(strConfig_File_Path)
misp = MISP(dictConfig["misp_url"], dictConfig["misp_key"])
event_obj = create_event_obj("test_event",  ["type:OSINT","OTX Vault", "tlp:green"])
event = misp.create_event(event_obj)

iocs = read_csv_file("6295d72c09bca73117c7b35c_export.csv")
for ioc in iocs:
    tag_arr = []
    tag_processing = ioc[2].split(";")
    tag_arr.append("OTX Vault")
    for tag in tag_processing:
        tag_arr.append(tag)
    temp_obj = create_attr_obj(ioc[0], CATEGORY[ioc[1]],IOC_TYPE[ioc[1]], "", "1", tag_arr)
    misp.add_attribute_event(event.id, temp_obj)

misp.publish_event(event.id)
input("delete event ?")
misp.delete_event(event.id)
