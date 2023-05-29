from pymisp import ExpandedPyMISP, MISPEvent
import os, urllib3, argparse

# disable warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ERROR CODE
ERR_PATH_NOT_FOUND = 0x2
ERR_CONFIG = 0x3
ERR_MISP = 0x4

def Argv_Parser():
    parser = argparse.ArgumentParser(description = "MISP Automation create event")
    parser.add_argument("-d", "--distrib",metavar = "", type=int, help="Distribution [0-3].")
    parser.add_argument("-i", "--info",metavar = "", help="Info.", required = True)
    parser.add_argument("-a", "--analysis",metavar = "", type=int, help="The analysis level [0-2].")
    parser.add_argument("-t", "--threat", metavar = "",type=int, help="The threat level ID [1-4].")
    parser.add_argument("-tags", metavar = "", nargs = "+")
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

def create_event(misp_API, info, tags = [], distrib=0, threat=1, analysis=0):
    if info == None or info == "":
        print("[!] Required Event info !!")
        exit(ERR_MISP)
    event = MISPEvent()
    event.distribution = distrib
    event.threat_level_id = threat
    event.analysis = analysis
    event.info = info
    for tag in tags:
        event.add_tag(tag)
    event = misp_API.add_event(event, pythonify=True)
    print("[+] Created ID: ", event.id)
    return event

if __name__ == "__main__":
    args = Argv_Parser()
    strConfig_File_Path = os.getcwd() + "/config.cfg"
    dictConfig = Get_Config(strConfig_File_Path)
    misp_API = Init(dictConfig["misp_url"], dictConfig["misp_key"])
    event = create_event(misp_API, args.info, args.tags, args.distrib, args.threat, args.analysis)
    print(event.uuid)  
    
    