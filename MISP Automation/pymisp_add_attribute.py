from pymisp import ExpandedPyMISP, MISPEvent, MISPAttribute
import os, urllib3, argparse

# disable warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ERROR CODE
ERR_PATH_NOT_FOUND = 0x2
ERR_CONFIG = 0x3
ERR_MISP = 0x4

def Argv_Parser():
    parser = argparse.ArgumentParser(description = "MISP Automation add event")
    parser.add_argument("-i", "--event_id", help="Event ID.", required = True, metavar="")
    parser.add_argument("-c", "--category", help= "Attribute category (Payload Delivery, Targeting data,...)", required = True, metavar="")
    parser.add_argument("-t", "--type", help="Type of Attribute (md5, sha256,...)", required=True, metavar="")
    parser.add_argument("-v", "--value", help="Value of Attribute", required=True, metavar="")
    parser.add_argument("-e", "--export", help="Set ids flag", required=True, metavar="")
    parser.add_argument("-comment", help="Comment for attribute", metavar="")
    parser.add_argument("-tags", help = "Tag for Attribute", nargs="+", default = [], metavar="")
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

def add_attribute_event(misp_API, event_id ,value, category, att_type, comment, to_ids, tags):
    misp_attribute = MISPAttribute()
    misp_attribute.value = str(value)
    misp_attribute.category = str(category)
    misp_attribute.type = str(att_type)
    misp_attribute.comment = str(comment)
    misp_attribute.to_ids = str(to_ids)
    for tag in tags:
        misp_attribute.add_tag(tag)
    r = misp_API.add_attribute(event_id, misp_attribute)
    if "errors" in r:
        print("[!] Fail to add attribute for event ", event_id)
    else:
        print("[+] Added attribute for event ", event_id)
        return r

if __name__ == "__main__":
    args = Argv_Parser()
    tags = ["test_tag","fun"]
    strConfig_File_Path = os.getcwd() + "/config.cfg"
    dictConfig = Get_Config(strConfig_File_Path)
    misp_API = Init(dictConfig["misp_url"], dictConfig["misp_key"])
    #add_attribute_event(misp_API, event.id, "098f6bcd4621d373cade4e832627b4f6", "Payload delivery", "md5", "", "1", ["bitch", "pls"])
    add_attribute_event(misp_API, args.event_id, args.value, args.category, args.type, args.comment, args.export, args.tags)
    