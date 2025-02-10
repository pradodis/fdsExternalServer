import json
import yaml
import grpc
import numpy as np
from urllib.request import urlopen
from pprint import pprint
from pyproj import Transformer
from . import commonDictionaries as cd
from dcs.net.v0 import net_pb2
from dcs.net.v0 import net_pb2_grpc
from dcs.coalition.v0 import coalition_pb2
from dcs.coalition.v0 import coalition_pb2_grpc

def get_location(ip_address):
    if ip_address == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + ip_address + '/json'
    res = urlopen(url)
    #response from url(if res==None then check connection)
    data = json.load(res)
    #will load the json response into data
    dataParcel = {}
    for attr in data.keys():
        #will print the data line by line
        dataParcel[attr] = data[attr]
    return dataParcel

class fetchGameData():
    def __init__(self, server_address, server_port, debug = False, **kwargs):
        # ACTIVE OBJECTS
        self.lLink = kwargs["luaLink"]
        self.r = kwargs["redis_conn"]
	    # YAML FILE
        with open('server_config.yml', 'r') as file:
            self.configFile = yaml.safe_load(file)
        # ALL ZONES
        query = self.lLink.send("return mist.DBs.zonesByName")
        self.allZones = json.loads(query.json)
        # MISSION INITIALIZATION
        self.initTgtObj = {}
        # MARK NUMBER
        self.markUpNumber = 0
        # INITIALIZING NET CONNECTION
        self.onLinePlayers = {}
        self.onLinePlayers["server"] = {}
        self.onLinePlayers["unit"] = {}
        self.netChannel = grpc.insecure_channel(f'{server_address}:{server_port}')
        self.netStub = net_pb2_grpc.NetServiceStub(self.netChannel)
        self.netStubUnit = coalition_pb2_grpc.CoalitionServiceStub(self.netChannel)
        self.onLinePlayersCheck()
        #-----------------------------------------------------------

        print("\033[92m" + "COMMOM GAME DATA INITIALIZED" + "\033[0m")

    def onLinePlayersCheck(self):
        self.onLinePlayers = {}
        self.onLinePlayers["server"] = {}
        self.onLinePlayers["unit"] = {}
        # Get Players
        request = net_pb2.GetPlayersRequest()
        response = self.netStub.GetPlayers(request)
        
        for playerData in response.players:
            keyDict = {
                "id": playerData.id,
                "name": playerData.name,
                "coalition": cd.coalition_code_network[str(playerData.coalition)],
                "slot": playerData.slot,
                "ping": playerData.ping,
                "remoteAddress": playerData.remote_address,
                "ucid": playerData.ucid
            }
            self.onLinePlayers["server"][playerData.name] = keyDict
            playerLocation = get_location(playerData.remote_address.split(":")[0])
            keyDict.update(playerLocation)  # Atualizando o dicionário com os dados de localização

            # Agora, armazene os dados no Redis. A chave do hash será o 'ucid' do jogador.
            hash_key = f"online_players:{playerData.ucid}"  # Definindo uma chave única para o jogador
            self.r.hmset(hash_key, keyDict)  # Armazenando o dicionário do jogador como um hash no Redis
            request_units = coalition_pb2.GetPlayerUnitsRequest()
            request_units.coalition = cd.grpc_coalition_enum[cd.coalition_code_network[str(playerData.coalition)]]
            response_units = self.netStubUnit.GetPlayerUnits(request_units)
            for unitData in response_units.units:
                dataDict = {
                    "id": unitData.id,
                    "name": unitData.name,
                    "coalition": cd.coalition_code_network[str(unitData.coalition)],
                    "position": {
                        "u": unitData.position.u, 
                        "v": unitData.position.v
                        },
                    "orientation": {
                        "heading": unitData.position.u, 
                        "yaw": unitData.position.v,
                        "pitch": unitData.position.v,
                        "roll": unitData.position.v
                        },
                    "type": unitData.type,
                    "category": cd.grpc_object_category[str(unitData.group.category)],
                    "playerName": unitData.player_name
                }
                self.onLinePlayers["unit"][unitData.name] = dataDict

        #print("\033[33m" + "└─► Online Players List Updated: " + str(len(response.players)) + " players online" + "\033[0m")
        return True