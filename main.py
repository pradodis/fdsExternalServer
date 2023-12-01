# FDS Server External Server 
# Tailored to be used with Rusty DCS gRPC Server
# By: Tsunami

import schedule
import time
import os
import asyncio
import grpc.aio
import redis
import threading
import yaml
from pprint import pprint
from modules import commonDictionaries as cd
import sys
sys.path.insert(0, '../modules')

# Import Modules
from modules import commonGameData as cGD
from modules import unitFetcher as uFet
from modules import eventFetcher as eFet
from modules import internalLuaLink as iLLink
#from modules import capturableRegions as iCapReg
from modules import zoneAttack as misZAttack

configFile = ''
with open('server_config.yml', 'r') as file:
    configFile = yaml.safe_load(file)

server_address = 'localhost'
server_port = 50051
redis_host = 'localhost'
redis_port = 6379
redis_db = 1


async def check_grpc_server(address, port, timeout = configFile["parameters"]["grpc_server_timeout"]):
    while True:
        try:
            async with grpc.aio.insecure_channel(f'{address}:{port}') as channel:
                await asyncio.wait_for(channel.channel_ready(), timeout=timeout)
            print(cd.bcolors.OKGREEN + f"---> DCS GRPC SERVER AT {address}:{port} IS UP AND RUNNING." + cd.bcolors.ENDC)
            break
        except (grpc.aio.AioRpcError, asyncio.TimeoutError) as e:
            print(cd.bcolors.RED + f"---> DCS gRPC SERVER AT {address}:{port} IS NOT RESPONDING." + cd.bcolors.ENDC)
            print(cd.bcolors.YELLOW + f"└─► TRYING TO RECONNECT IN {configFile['parameters']['grpc_server_reconection_time']} SECONDS..." + cd.bcolors.ENDC)
            await asyncio.sleep(configFile["parameters"]["grpc_server_reconection_time"])

async def check_redis_server(host, port, db, timeout=configFile["parameters"]["redis_timeout"]):
    r = redis.StrictRedis(host=host, port=port, db=db)
    while True:
        try:
            await asyncio.wait_for(run_in_executor(r.ping), timeout=configFile["parameters"]["grpc_server_timeout"])
            print(cd.bcolors.OKGREEN + f"---> REDIS SERVER AT {host}:{port}, db={db} IS UP AND RUNNING." + cd.bcolors.ENDC)
            break
        except (redis.exceptions.RedisError, asyncio.TimeoutError) as e:
            print(cd.bcolors.RED + f"---> REDIS SERVER AT {host}:{port}, db={db} IS NOT RESPONDING." + cd.bcolors.ENDC)
            print(cd.bcolors.YELLOW + f"└─► TRYING TO RECONNECT IN {configFile['parameters']['redis_reconection_time']} SECONDS..." + cd.bcolors.ENDC)
            await asyncio.sleep(configFile["parameters"]["redis_reconection_time"])

async def run_in_executor(func, *args):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, func, *args)
    return result

async def connection_check():
    await asyncio.gather(
        check_grpc_server(server_address, server_port),
        check_redis_server(redis_host, redis_port, redis_db)
    )

def redis_keyspace_notification(channel):
    for message in channel.listen():
        print(f"RECEIVED ORDER: {message}")
        # Verifica se a mensagem é do tipo que estamos interessados.
        if message['type'] == 'pmessage':
            # Você pode processar `message['data']` ou `message['channel']` conforme necessário.
            key_changed = message['data']
            if key_changed == b'set':
                # A chave que estamos monitorando mudou, atualize a variável global ou chame uma função.
                global_state['arguments'] = r.get('arguments')
                print(f"Key 'arguments' changed! New value: {global_state['arguments']}")

# MAIN
if __name__ == '__main__':
    os.system('color')
    print(cd.bcolors.BLUE + "==========================================================================================" + cd.bcolors.ENDC)
    print(cd.bcolors.BLUE + "==========================================================================================\n" + cd.bcolors.ENDC)
    print(cd.bcolors.BLUE + "//////////////////////     ////////////////////                   ////////////////////    " + cd.bcolors.ENDC)
    print(cd.bcolors.BLUE + "//////////////////////     //////////////////////               //////////////////////    " + cd.bcolors.ENDC)
    print(cd.bcolors.BLUE + "/////                      /////                /////          /////                      " + cd.bcolors.ENDC)
    print(cd.bcolors.BLUE + "/////                      /////                 /////        /////                       " + cd.bcolors.ENDC)
    print(cd.bcolors.BLUE + "/////                      /////                  /////       /////                       " + cd.bcolors.ENDC)
    print(cd.bcolors.BLUE + "/////                      /////                   /////       /////                      " + cd.bcolors.ENDC)
    print(cd.bcolors.BLUE + "/////                      /////                   /////         /////                    " + cd.bcolors.ENDC)
    print(cd.bcolors.BLUE + "//////////////////////     /////                   /////           /////                  " + cd.bcolors.ENDC)
    print(cd.bcolors.RED + "//////////////////////     /////                   /////              /////               " + cd.bcolors.ENDC)
    print(cd.bcolors.RED + "/////                      /////                   /////                /////             " + cd.bcolors.ENDC)
    print(cd.bcolors.RED + "/////                      /////                   /////                   /////          " + cd.bcolors.ENDC)
    print(cd.bcolors.RED + "/////                      /////                  /////                       /////       " + cd.bcolors.ENDC)
    print(cd.bcolors.RED + "/////                      /////                 /////                          /////     " + cd.bcolors.ENDC)
    print(cd.bcolors.RED + "/////                      /////                /////                           /////     " + cd.bcolors.ENDC)
    print(cd.bcolors.RED + "/////                      //////////////////////            //////////////////////       " + cd.bcolors.ENDC)
    print(cd.bcolors.RED + "/////                      ////////////////////              ////////////////////         " + cd.bcolors.ENDC)
    print(cd.bcolors.RED + "\n==========================================================================================" + cd.bcolors.ENDC)
    print(cd.bcolors.RED + "==========================================================================================\n" + cd.bcolors.ENDC)
    print(cd.bcolors.OKGREEN + "-------------------------------  INITIALIZING FDS SERVER  --------------------------------" + cd.bcolors.ENDC)

    
    asyncio.run(connection_check())
    
    #REDIS INIT
    r = redis.Redis(host=redis_host, port=redis_port, db=1)
    # Variável global para monitorar o estado.
    global_state = {'arguments': None}
    p = r.pubsub(ignore_subscribe_messages=True)
    p.psubscribe('__keyspace@1__:arguments')
    # Inicia uma nova thread para ouvir as notificações de keyspace
    threading.Thread(target=redis_keyspace_notification, args=(p,), daemon=True).start()

    #Loading Modules
    print("\n▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  LOADING MODULES  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    iLuaLink = iLLink.internalLuaLink(server_address, server_port) # LUA CONNECTION
    commonGD = cGD.fetchGameData(server_address, server_port, luaLink = iLuaLink, redis_conn = r) # COMMON GAME DATA
    uFetch = uFet.unitFetcher(server_address, server_port) # UNIT CONNECTION
    eFetch = eFet.eventFetcher(server_address, server_port, commom_game_data = commonGD) # EVENT CONNECTION
    #iCR = iCapReg.capturableRegions(server_address, server_port, common = commonGD, luaLink = iLuaLink) # CAPTURABLE ZONES MODULE
    print("▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  MODULES LOADED  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n")
    
    #MAIN MISSION MODULE
    mainMission = misZAttack.missionZoneAttackPVP(iLuaLink, commom_game_data = commonGD, redis_conn = r)

    # Starting Streams and Lua Link
    eFetch.fetch()
    uFetch.fetch()
    iLuaLink.send("return True")

    # Schedulling events
    schedule.every().second.do(eFetch.evaluateEvents)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print(cd.bcolors.WARNING + "------------------------------  SHUTTING DOWN SERVER  ------------------------------" + cd.bcolors.ENDC)
        r.close()
        print(cd.bcolors.WARNING + "------------------------------   SHUTDOWN COMPLETED  -------------------------------" + cd.bcolors.ENDC)