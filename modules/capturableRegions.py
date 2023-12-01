import yaml
import grpc

# Import the generated gRPC classes
from dcs.trigger.v0 import trigger_pb2
from dcs.trigger.v0 import trigger_pb2_grpc

class capturableRegions:
    def __init__(self, server_address, server_port, **kwargs):
        # Active Objects
        self.common = kwargs["common"]
        self.lLink = kwargs["luaLink"]
        # YAML Initialization
        with open('server_config.yml', 'r') as file:
            configFile = yaml.safe_load(file)
        self.colorDict = {
            'blue': configFile['capturableRegions']['markColorDict']['blue'],
            'red': configFile['capturableRegions']['markColorDict']['red'],
            'neutral': configFile['capturableRegions']['markColorDict']['neutral']
            }
        self.textColorDict = {
            'blue': configFile['capturableRegions']['textColorDict']['blue'],
            'red': configFile['capturableRegions']['textColorDict']['red'],
            'neutral': configFile['capturableRegions']['textColorDict']['neutral']
            }
        # CAPTURABLE ZONES IN COMMONS
        self.common.contestedRegionNames = configFile['capturableRegions']['names']
        self.common.capZones = {}
        for capName in self.common.contestedRegionNames:
            self.common.capZones[capName] = {'textDraw': [], 'zoneDraw': []}
            for name in self.allZones.keys():
                if name.startswith('draw' + capName):
                    if 'Text' in name:
                        self.common.capZones[capName]['textDraw'].append(name)
                    else:
                        self.common.capZones[capName]['zoneDraw'].append(name)
        # gRPC Initialization
        self.channel = grpc.insecure_channel(f'{server_address}:{server_port}')
        self.stub = trigger_pb2_grpc.TriggerServiceStub(self.channel)
        # Region Status Initialization
        self.common.regionStatus = {}
        luaAllCommands = ""
        for region in self.common.contestedRegionNames:
            self.common.regionStatus[region] = {}
            self.common.regionStatus[region]['owner'] = 'neutral'
            self.common.regionStatus[region]['income'] = configFile['capturableRegions']['minRegionIncome']
            self.common.regionStatus[region]['capture'] = 0
            luaStringDrawText = self.drawRegionInfo(region, self.common.regionStatus[region]['income'], self.common.regionStatus[region]['owner'])
            # CREATING CAPTURE CIRCLES
            captureCircle = self.common.allZones['regionCap' + region]
            self.common.markUpNumber += 1
            luaStringCircle = "trigger.action.circleToAll(-1, " + str(self.common.markUpNumber) + ", " + "trigger.misc.getZone('" + str('regionCap' + region) + "').point, " + str(captureCircle['radius']) + ", {0, 0, 0, 1}, {0, 0, 0, 0}, 1, true)"
            luaAllCommands = luaAllCommands + luaStringDrawText + " " + luaStringDrawText + " " + luaStringCircle + " "
        query = self.lLink.send(luaAllCommands)
        # INIT END
        print("\033[92m" + "CAPTURABLE REGIONS INITIALIZED" + "\033[0m")
            
    def drawRegionInfo(self, regionName, regionValue, ownerTeam):
        self.common.markUpNumber += 1
        # ERASING OLD PANELS
        if "shapeIds" in self.common.regionStatus[regionName]:
            request = trigger_pb2.RemoveMarkRequest()
            request.id = self.common.regionStatus[regionName]["shapeIds"][0]
            response = self.stub.RemoveMark(request)
            request.id = self.common.regionStatus[regionName]["shapeIds"][1]
            response = self.stub.RemoveMark(request)
        # ASSEMBLING LUA STRING FOR MARKUPTOALL
        luaStringDraw = "7, -1, " + str(self.common.markUpNumber) + ", "
        for index in range(len(self.common.capZones[regionName]['zoneDraw'])):
            luaStringDraw = luaStringDraw + "trigger.misc.getZone('" + "draw" +  regionName + str(index+1)+"').point" + ", "
        luaStringDraw = luaStringDraw + "{0, 0, 0, 1}, {" + str(self.colorDict[ownerTeam])[1:-1] + "}, 4"
        luaStringDraw = "trigger.action.markupToAll(" + luaStringDraw + ")"
        shapeNumber = self.common.markUpNumber
        self.common.markUpNumber += 1
        textNumber = self.common.markUpNumber
        # ASSEMBLING LUA STRING FOR TEXTTOALL
        luaStringText = "trigger.action.textToAll(-1, " + str(self.common.markUpNumber) + ", " + "trigger.misc.getZone('" + str(self.common.capZones[regionName]['textDraw'][0]) + "').point, "
        luaStringText = luaStringText + "{" + str(self.textColorDict[ownerTeam])[1:-1] + "}, {0, 0, 0, 0}, 20, true , '" + regionName + "\\n$" + str(regionValue) + "')"
        self.common.regionStatus[regionName]["shapeIds"] = [shapeNumber, textNumber]
        return luaStringDraw + " " + luaStringText