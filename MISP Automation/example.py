from pymisp_create_event import create_event
from pymisp_delete_event import delete_event_or_attr
from pymisp_add_attribute import add_attribute_event
from pymisp import ExpandedPyMISP, MISPEvent
import os

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

def Init(url, key):
    return ExpandedPyMISP(url, key, False, "json", proxies=None)

strConfig_File_Path = os.getcwd() + "/config.cfg"
dictConfig = Get_Config(strConfig_File_Path)
misp_API = Init(dictConfig["misp_url"], dictConfig["misp_key"])
event = create_event(misp_API, "test create")
attr_arr = []
temp = add_attribute_event(misp_API, event.id, "098f6bcd4621d373cade4e832627b4f6", "Payload delivery", "md5", "", "1", ["bitch", "pls"])
attr_arr.append(temp["AttributeTag"][0]["attribute_id"])
temp = add_attribute_event(misp_API, event.id, "098f6bcd4621d373cade4e832627b422", "Payload delivery", "md5", "", "1", ["bitch", "pls"])
attr_arr.append(temp["AttributeTag"][0]["attribute_id"])
input("delete first attr")
delete_event_or_attr(misp_API,0,attr_arr[0])
input("delete ?")
delete_event_or_attr(misp_API, event.id, 0)