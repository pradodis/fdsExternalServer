# FDS Server External Server 
# Tailored to be used with Rusty DCS gRPC Server
# By: Tsunami

import schedule
import time
import os
import grpc

class bcolors:
    HEADER = "\033[95m"
    BLUE = "\033[34m"
    RED = "\033[31m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

server_address = 'localhost'
server_port = 50051

def initializeUnitFetcher():
    from modules import unitFetcher as uFet
    uFetch = uFet.unitFetcher(server_address, server_port)
    schedule.every(5).seconds.do(uFetch.fetch)
    print(bcolors.OKGREEN + "UNIT FETCHER INITIALIZED" + bcolors.ENDC)
    return uFetch

def initializeEventFetcher():
    from modules import eventFetcher as eFet
    eFetch = eFet.eventFetcher(server_address, server_port)
    schedule.every(5).seconds.do(eFetch.fetch)
    print(bcolors.OKGREEN + "EVENT FETCHER INITIALIZED" + bcolors.ENDC)
    return eFetch

def initializeInternalLuaLink():
    from modules import internalLuaLink as iLLink
    iLuaLink = iLLink.internalLuaLink(server_address, server_port)
    print(bcolors.OKGREEN + "INTERNAL LUA LINK INITIALIZED" + bcolors.ENDC)
    return iLuaLink

# MAIN
if __name__ == '__main__':
    os.system('color')
    print(bcolors.BLUE + "==========================================================================================" + bcolors.ENDC)
    print(bcolors.BLUE + "==========================================================================================\n" + bcolors.ENDC)
    print(bcolors.BLUE + "//////////////////////     ////////////////////                   ////////////////////    " + bcolors.ENDC)
    print(bcolors.BLUE + "//////////////////////     //////////////////////               //////////////////////    " + bcolors.ENDC)
    print(bcolors.BLUE + "/////                      /////                /////          /////                      " + bcolors.ENDC)
    print(bcolors.BLUE + "/////                      /////                 /////        /////                       " + bcolors.ENDC)
    print(bcolors.BLUE + "/////                      /////                  /////       /////                       " + bcolors.ENDC)
    print(bcolors.BLUE + "/////                      /////                   /////       /////                      " + bcolors.ENDC)
    print(bcolors.BLUE + "/////                      /////                   /////         /////                    " + bcolors.ENDC)
    print(bcolors.BLUE + "//////////////////////     /////                   /////           /////                  " + bcolors.ENDC)
    print(bcolors.RED + "//////////////////////     /////                   /////              /////               " + bcolors.ENDC)
    print(bcolors.RED + "/////                      /////                   /////                /////             " + bcolors.ENDC)
    print(bcolors.RED + "/////                      /////                   /////                   /////          " + bcolors.ENDC)
    print(bcolors.RED + "/////                      /////                  /////                       /////       " + bcolors.ENDC)
    print(bcolors.RED + "/////                      /////                 /////                          /////     " + bcolors.ENDC)
    print(bcolors.RED + "/////                      /////                /////                           /////     " + bcolors.ENDC)
    print(bcolors.RED + "/////                      //////////////////////            //////////////////////       " + bcolors.ENDC)
    print(bcolors.RED + "/////                      ////////////////////              ////////////////////         " + bcolors.ENDC)
    print(bcolors.RED + "\n==========================================================================================" + bcolors.ENDC)
    print(bcolors.RED + "==========================================================================================\n" + bcolors.ENDC)
    print(bcolors.OKGREEN + "-------------------------------  INITIALIZING FDS SERVER  --------------------------------" + bcolors.ENDC)

    print("\nLOADING MODULES")
    uFetch = initializeUnitFetcher()
    eFetch = initializeEventFetcher()
    iLuaLink = initializeInternalLuaLink()
    print("MODULES LOADED\n\n")

    iLuaLink.send("ping('oi')")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print(bcolors.WARNING + "------------------------------  SHUTTING DOWN SERVER  ------------------------------" + bcolors.ENDC)
        print(bcolors.WARNING + "------------------------------   SHUTDOWN COMPLETED  -------------------------------" + bcolors.ENDC)