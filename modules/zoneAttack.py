import json
import random
import matplotlib.pyplot as plt
import matplotlib.path as mpltPath
import math
import yaml
import grpc
import numpy as np
from urllib.request import urlopen
from pprint import pprint
from pyproj import Transformer
from . import command_strings_lib as cstrlib
from . import commonDictionaries as cd
from dcs.net.v0 import net_pb2
from dcs.net.v0 import net_pb2_grpc

def get_random_point_in_circle(cx, cy, r):
    angle = random.uniform(0, 2 * math.pi)
    sqrt_random_radius = math.sqrt(random.uniform(0, 1))
    radius = sqrt_random_radius * r
    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)
    return (x, y)

def is_point_in_circ(p1, p2, distancia):
    dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    return dist < distancia

def plot_objects_position(box_list):
    x_coords = [ponto['x'] for subvetor in box_list["bounding"] for ponto in subvetor]
    y_coords = [ponto['y'] for subvetor in box_list["bounding"] for ponto in subvetor]
    xc_coords = [point['x'] for point in box_list["center"]]
    yc_coords = [point['y'] for point in box_list["center"]]
    # Cria a figura e o eixo no matplotlib.
    fig, ax = plt.subplots()
    # Plota os pontos.
    ax.scatter(x_coords, y_coords, color='blue')  # Pontos azuis.
    ax.scatter(xc_coords, yc_coords, color='red')  # Pontos azuis.
    # Define o título e os rótulos dos eixos.
    ax.set_title('Pontos representando os vértices do quadrado')
    ax.set_xlabel('Coordenada X')
    ax.set_ylabel('Coordenada Y')
    # Configura os limites dos eixos para melhor visualização, se necessário.
    ax.axis('equal')  # Isso garante que a proporção de 1:1 seja mantida nos eixos.
    plt.show()

class missionZoneAttackPVP:
    def __init__(self, lua_link_module, **kwargs):
        self.commomGD = kwargs["commom_game_data"]
        self.r = kwargs["redis_conn"]
        self.llink = lua_link_module
	    # YAML FILE
        with open('server_config.yml', 'r') as file:
            self.configFile = yaml.safe_load(file)

        #Init Static
        deviation0 = 150.0
        angle0 = 6.6
        deviationHangarr = 120.0
        angleHangarr = -3.1415/180*40
        deviationHangarc = 120.0
        angleHangarc = -3.1415/180*130
        
        deviationFuelr = 70.0
        angleFuelr = 3.1415/180*70
        deviationFuelc = 70.0
        angleFuelc = 3.1415/180*160
        
        haeding4All = 45.0

        nCP = 1
        nHangarr = 2
        nHangarc = 2
        nFuelr = 2
        nFuelc = 3

        self.tgtQty = {
            "paratrooperAKS74" : [self.configFile["mainMission"]["unitsZones"]["InfAK"], 'Inf_AK'], 
            "paratrooperRPG16" : [self.configFile["mainMission"]["unitsZones"]["InfRPG"], 'Inf_RPG'],
            "ural4320T" : [self.configFile["mainMission"]["unitsZones"]["ArmTrucks"],'STrucks'], 
            "BMP1" : [self.configFile["mainMission"]["unitsZones"]["ArmBMP1"],'Arm_BMP1'], 
            "BMP2" : [self.configFile["mainMission"]["unitsZones"]["ArmBMP2"],'Arm_BMP2'], 
            "T55" : [self.configFile["mainMission"]["unitsZones"]["ArmT55"],'Arm_T55'] , 
            "T72B" : [self.configFile["mainMission"]["unitsZones"]["ArmT72"],'Arm_T72'], 
            "T80UD" : [self.configFile["mainMission"]["unitsZones"]["ArmT80"],'Arm_T80'] , 
            "ZSU234Shilka" : [np.random.randint(self.configFile["mainMission"]["unitsZones"]["AAA"][0], self.configFile["mainMission"]["unitsZones"]["AAA"][1]+1),'AAA'], 
            "S6Tunguska" : [np.random.randint(self.configFile["mainMission"]["unitsZones"]["AATung"][0], self.configFile["mainMission"]["unitsZones"]["AATung"][1]+1),'AA_Tung'], 
            "Strela19P31" : [np.random.randint(self.configFile["mainMission"]["unitsZones"]["AAStrela1"][0], self.configFile["mainMission"]["unitsZones"]["AAStrela1"][1]+1),'AA_Strela1'], 
            "Strela10M3" : [np.random.randint(self.configFile["mainMission"]["unitsZones"]["AAStrela2"][0], self.configFile["mainMission"]["unitsZones"]["AAStrela2"][1]+1),'AA_Strela2'], 
            "SA18IglaSmanpad" : [np.random.randint(self.configFile["mainMission"]["unitsZones"]["AAIgla"][0], self.configFile["mainMission"]["unitsZones"]["AAIgla"][1]+1),'AA_Igla'],
            "Tor9A331" : [np.random.randint(self.configFile["mainMission"]["unitsZones"]["AATor"][0], self.configFile["mainMission"]["unitsZones"]["AATor"][1]+1),'AA_Tor']
        }
        self.zAttackZones = {'joinedZones': {}, 'blueZones': ['Blue Zone 1','Blue Zone 2'], 'redZones': ['Red Zone 1','Red Zone 2'], 'markUpNumber': 0, 'farpTextID': 0}
        self.tgtObj = {'blue': {}, 'red': {}}

        command_string = 'target_data = {} \n'
        # Processando as zonas azuis
        for blue_zone in self.zAttackZones['blueZones']:
            command_string = command_string + f"target_data['{blue_zone}'] = " + "{['struct'] = {}, ['unit'] = {}} \n"
            self.zAttackZones['joinedZones'][blue_zone] = 1
            if 'blue' not in self.tgtObj:  # Verifique se a chave 'blue' existe em tgtObj; se não, crie-a.
                self.tgtObj['blue'] = {}
            self.tgtObj['blue'][blue_zone] = {}

        # Processando as zonas vermelhas
        for red_zone in self.zAttackZones['redZones']:
            command_string = command_string + f"target_data['{red_zone}'] = " + "{['struct'] = {}, ['unit'] = {}} \n"
            self.zAttackZones['joinedZones'][red_zone] = 0
            if 'red' not in self.tgtObj:  # Verifique se a chave 'red' existe em tgtObj; se não, crie-a.
                self.tgtObj['red'] = {}
            self.tgtObj['red'][red_zone] = {}

        # Definição de tipos estáticos, similar ao código Lua
        static_types = {
            'types': ['.Command Center', 'Shelter', 'Fuel tank'],
            'number': {'.Command Center': [nCP], 'Shelter': [nHangarr, nHangarc], 'Fuel tank': [nFuelr, nFuelc]},
            'cat': {'.Command Center': [4], 'Shelter': [4], 'Fuel tank': [4]},
            'dist': {
                '.Command Center': [deviation0, angle0],
                'Shelter': [[deviationHangarr, angleHangarr], [deviationHangarc, angleHangarc]],
                'Fuel tank': [[deviationFuelr, angleFuelr], [deviationFuelc, angleFuelc]]
            },
            'column': {'.Command Center': [nCP], 'Shelter': [nHangarr, nHangarc], 'Fuel tank': [nFuelr, nFuelc]}
        }


        for tz, cc in self.zAttackZones['joinedZones'].items():
            zone_point = self.commomGD.allZones[tz]["point"]
            add_point = {
                'x': zone_point["x"],
                'z': zone_point["z"]
            }

            box_list = {"bounding" : [], "center": []}
            for i in static_types['types']:
                if i == '.Command Center':
                    infoAdd = {}
                    infoAdd["zonename"] = tz
                    infoAdd["country"] = cc
                    infoAdd["category"] = static_types["cat"][i][0]
                    infoAdd["x"] = add_point["x"]
                    infoAdd["y"] = add_point["z"]
                    infoAdd["type"] = i
                    infoAdd["heading"] = haeding4All  
                    box_pos = []      
                    for vert in range(4):
                        angle_rad = math.radians(infoAdd['heading'] + 45.0 + 90.0 * (vert+1))
                        vertex = {
                            'x': infoAdd['x'] + 40.0 * math.cos(angle_rad),
                            'y': infoAdd['y'] + 40.0 * math.sin(angle_rad)
                        }
                        box_pos.append(vertex)
                    if cc == 1:
                        self.tgtObj['blue'][tz] = [{'x': infoAdd['x'], 'y': infoAdd['y']}, box_pos]
                    else:
                        self.tgtObj['red'][tz] = [{'x': infoAdd['x'], 'y': infoAdd['y']}, box_pos]
                    box_list["bounding"].append(box_pos)
                    box_list["center"].append({'x': infoAdd['x'], 'y': infoAdd['y'], "radius": 40})
                    command_string = command_string + cstrlib.generate_objective_structures(infoAdd)
                else:
                    for r in range(0, static_types["column"][i][0]):
                        for c in range(0, static_types["column"][i][1]):
                            addingX = (r+1)*(static_types["dist"][i][0][0]*math.cos(static_types["dist"][i][0][1]))+c*(static_types["dist"][i][1][0]*math.cos(static_types["dist"][i][1][1]))
                            addingY = (r+1)*(static_types["dist"][i][0][0]*math.sin(static_types["dist"][i][0][1]))+c*(static_types["dist"][i][1][0]*math.sin(static_types["dist"][i][1][1]))
                            infoAdd = {}
                            infoAdd["zonename"] = tz
                            infoAdd["country"] = cc
                            infoAdd["category"] = static_types["cat"][i][0]
                            infoAdd["x"] = add_point["x"] + addingX
                            infoAdd["y"] = add_point["z"] + addingY
                            infoAdd["type"] = i
                            infoAdd["heading"] = haeding4All   
                            box_pos = []        
                            for vert in range(4):
                                angle_rad = math.radians(infoAdd['heading'] + 45.0 + 90.0 * (vert+1))
                                vertex = {
                                    'x': infoAdd['x'] + 40.0 * math.cos(angle_rad),
                                    'y': infoAdd['y'] + 40.0 * math.sin(angle_rad)
                                }
                                box_pos.append(vertex)
                            if cc == 1:
                                self.tgtObj['blue'][tz] = [{'x': infoAdd['x'], 'y': infoAdd['y']}, box_pos]
                            else:
                                self.tgtObj['red'][tz] = [{'x': infoAdd['x'], 'y': infoAdd['y']}, box_pos]
                            box_list["bounding"].append(box_pos)
                            box_list["center"].append({'x': infoAdd['x'], 'y': infoAdd['y'], "radius": 40})
                            command_string = command_string + cstrlib.generate_objective_structures(infoAdd)
            for unc, qt in self.tgtQty.items():
                for unit_number in range(1, qt[0] + 1):
                    check_p = True
                    it = 0
                    while check_p:
                        check_p = False
                        born_point = get_random_point_in_circle(add_point["x"],add_point["z"], self.commomGD.allZones[tz]["radius"])
                        for c_obj in box_list["center"]:
                            if not check_p: 
                                check_p = is_point_in_circ(born_point, (c_obj["x"], c_obj["y"]), c_obj["radius"]+10)
                        it += 1
                        if it > 100:
                            check_p = False
                    heading = random.uniform(0.0, 359.0)  
                    mock_name = 'Blue_' + qt[1] if cc == 1 else 'Red_' + qt[1]
                    infoAdd = {}
                    infoAdd["zonename"] = tz
                    infoAdd["mockname"] = mock_name
                    infoAdd["country"] = cc
                    infoAdd["category"] = 2
                    infoAdd["x"] = born_point[0]
                    infoAdd["y"] = born_point[1]
                    infoAdd["type"] = i
                    infoAdd["heading"] = heading  

                    box_pos = []      
                    for vert in range(4):
                        angle_rad = math.radians(heading + 45.0 + 90.0 * (vert+1))
                        vertex = {
                            'x': born_point[0] + 10.0 * math.cos(angle_rad),
                            'y': born_point[1] + 10.0 * math.sin(angle_rad)
                        }
                        box_pos.append(vertex)

                    team = 'blue' if cc == 1 else 'red'
                    self.tgtObj[team][tz].append({
                        'name': 'name',
                        'position': {'x': born_point[0], 'y': born_point[1]},
                        'category': "nulo"
                    })     
                    box_list["bounding"].append(box_pos)
                    box_list["center"].append({'x': born_point[0], 'y': born_point[1], "radius": 10})      
                    command_string = command_string + cstrlib.generate_objective_groundUnits(infoAdd)       
            #plot_objects_position(box_list)
        command_string = command_string + f"return target_data"
        #print(command_string)  
        target_data = self.llink.send(command_string)
        rcv_file = target_data.SerializeToString() 
        rcv_file_initial_char = rcv_file.find(b'{')
        if rcv_file_initial_char != -1:
            rcv_file_processed = rcv_file[rcv_file_initial_char:]
        else:
            rcv_file_processed = rcv_file
        rcv_file = json.loads(rcv_file_processed)

        # Inicialize o pipeline
        pipeline = self.r.pipeline()

        for zone, data in rcv_file.items():
            for uniorstruct, dataentity in data.items():
                for entity in dataentity:
                    entitydata = entity
                    groupid_case = entity["groupId"]
                    if uniorstruct == 'unit': 
                        entitydata = entity['units'][0]
                    keys_dictionary ={
                        "type": entitydata["type"],
                        "groupId": groupid_case,
                        "y": entitydata["y"],
                        "x": entitydata["x"],
                        "name": entitydata["name"],
                        "unitId": entitydata["unitId"]
                    }
                    # Cria a chave e a processa para ficar em minúsculas e sem espaços
                    key = ''.join(f"targetzones:{str(zone)}:{str(uniorstruct)}:{str(entitydata['unitId'])}".lower().split())
                    # Armazena a string JSON serializada no hash dentro do pipeline
                    pipeline.hmset(key, keys_dictionary)
        pipeline.hmset(key, keys_dictionary)

        # Execute todas as operações no pipeline de uma só vez
        pipeline.execute()

        self.r.set("ongoing_zoneassault", "True")
        print("\033[94m" + "MAIN MISSION LOADED: ZONE ASSAULT PVP" + "\033[0m\n")