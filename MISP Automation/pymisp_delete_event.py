from pymisp import ExpandedPyMISP, MISPEvent
import os, urllib3, argparse

# disable warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ERROR CODE
ERR_PATH_NOT_FOUND = 0x2
ERR_CONFIG = 0x3
ERR_MISP = 0x4

def Argv_Parser():
    parser = argparse.ArgumentParser(description = "MISP Automation delete event")
    parser.add_argument("-e", "--event", help="Event ID.", required = True)
    parser.add_argument("-a", "--attribute", help="Attribute ID.")
    args = parser.parse_args()
    return args

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

def delete_event_or_attr(misp_API, event_id, attr_id):
    if event_id != 0:
        result = misp_API.delete_event(event_id)
    elif attr_id != 0:
        result = misp_API.delete_attribute(attr_id)
    if "errors" in result:
        if attr_id == 0:
            print("[!] Fail to delete event ", event_id)
        elif event_id == 0:
            print("[!] Fail to delete attribute ", attr_id)
    else:
        if attr_id == 0:
            print("[+] Success deleted event ", event_id)
        elif event_id == 0:
            print("[+] Success deleted attribute ", attr_id)

if __name__ == "__main__":
    args = Argv_Parser()
    strConfig_File_Path = os.getcwd() + "/config.cfg"
    dictConfig = Get_Config(strConfig_File_Path)
    misp_API = Init(dictConfig["misp_url"], dictConfig["misp_key"])
    if args.event:
        delete_event_or_attr(misp_API,args.event, 0)
    else:
        delete_event_or_attr(misp_API, 0, args.attribute)
    