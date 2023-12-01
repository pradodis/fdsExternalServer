import json
import yaml
import grpc
import numpy as np
from urllib.request import urlopen
from pprint import pprint
from pyproj import Transformer
from dcs.net.v0 import net_pb2
from dcs.net.v0 import net_pb2_grpc

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
        self.netChannel = grpc.insecure_channel(f'{server_address}:{server_port}')
        self.netStub = net_pb2_grpc.NetServiceStub(self.netChannel)
        self.onLinePlayersCheck()
        #-----------------------------------------------------------

        print("\033[92m" + "COMMOM GAME DATA INITIALIZED" + "\033[0m")

    def onLinePlayersCheck(self):
        request = net_pb2.GetPlayersRequest()
        response = self.netStub.GetPlayers(request)
        for playerData in response.players:
            keyDict = {
                "id": playerData.id,
                "name": playerData.name,
                "coalition": playerData.coalition,
                "slot": playerData.slot,
                "ping": playerData.ping,
                "remoteAddress": playerData.remote_address,
                "ucid": playerData.ucid
            }
            self.onLinePlayers[playerData.ucid] = keyDict
            playerLocation = get_location(playerData.remote_address.split(":")[0])
            keyDict.update(playerLocation)  # Atualizando o dicionário com os dados de localização

            # Agora, armazene os dados no Redis. A chave do hash será o 'ucid' do jogador.
            hash_key = f"online_players:{playerData.ucid}"  # Definindo uma chave única para o jogador
            self.r.hmset(hash_key, keyDict)  # Armazenando o dicionário do jogador como um hash no Redis

        print("\033[33m" + "└─► Online Players List Updated: " + str(
            len(response.players)) + " players online" + "\033[0m")
        return True

'''
    FDS.joinedZones = {}
	zones = mist.DBs.zonesByName

	for i=1, #FDS.blueZones,1 do
		FDS.joinedZones[FDS.blueZones[i]]= 1
        tgtObj.blue[FDS.blueZones[i]] = {}
	end

	for i= 1, #FDS.redZones, 1 do
		FDS.joinedZones[FDS.redZones[i]]= 0
        tgtObj.red[FDS.redZones[i]] = {}
	end

	FDS.markUpNumber = FDS.markUpNumber + 1
	trigger.action.textToAll(-1, FDS.markUpNumber, trigger.misc.getZone('cZone_1').point, {1, 1, 1, 1} , {1, 1, 1, 0.0} , 20, true , 'Capturable FARP: Neutral' )
	FDS.farpTextID = FDS.markUpNumber

	for i = 1,2,1 do
		activePl = coalition.getPlayers(i)
		if #activePl ~= 0 then
			for j,k in pairs(activePl) do
				if i == 1 then
					gp = k:getGroup()
					gpId = gp:getID()
					gpCoa = k:getCoalition()
					gpPN = k:getPlayerName()
					gpName = k:getName()
					gpUcid = FDS.retrieveUcid(gpPN,FDS.isName)
					local cleanCargo = false
					if k:getCategory() == 1 then
						for i,j in pairs(FDS.heliSlots) do
							if k:getDesc().typeName == i then
								cleanCargo = true
							end
						end
						if cleanCargo then
							FDS.cargoList[tostring(k:getName())] = {} 
							FDS.valuableList[tostring(k:getName())] = {} 
						end
					end
					local msg = {}
					msg.text = gpPN .. ', you can help your team by:\n\n - Attacking ground targets in enemy zones (AG mission)(See map or [radio]>[F10]>[Where to attack]).\n\n - Attacking the enemy air transports in enemy supply route (AA mission) (See map).\n - Rescuing point around the map with helicopters (Helo rescue mission).\n - Killing enemy players in the process is always a good idea!\n\n - Visit our website: "https://dcs.comicorama.com/" for server and players stats.\n - Join our Discord community at FDS Server (Link available in the briefing). \nAn explanation about this server is available on our youtube channel: "FDS Server - DCS".'
					msg.displayTime = 60
					msg.sound = 'Welcome.ogg'
					mist.scheduleFunction(missionCommands.addCommandForGroup,{gpId,'Current War Status',nil, FDS.warStatus, {gpId, gpCoa, gpPN}},timer.getTime()+FDS.wtime)
					mist.scheduleFunction(missionCommands.addCommandForGroup,{gpId,'Where to Attack',nil, FDS.whereStrike, {gpId, gpCoa, gpName}},timer.getTime()+FDS.wtime)
					mist.scheduleFunction(missionCommands.addCommandForGroup,{gpId,'Where to Defend',nil, FDS.whereDefend, {gpId, gpCoa, gpName}},timer.getTime()+FDS.wtime)
					mist.scheduleFunction(missionCommands.addCommandForGroup,{gpId,'Drop Zones',nil, FDS.whereDropZones, {gpId, gpCoa, gpName}},timer.getTime()+FDS.wtime)
					FDS.addCreditsOptions(gp)
					FDS.addJtacOption(gp)
					FDS.addTroopManagement(gp)
					mist.scheduleFunction(trigger.action.outTextForGroup,{gpId,msg.text,msg.displayTime},timer.getTime()+FDS.wtime)
					mist.scheduleFunction(trigger.action.outSoundForGroup,{gpId,msg.sound},timer.getTime()+FDS.wtime)
					if i == 1 then 
						FDS.teamPoints['red']['Players'][gpPN] = 0
					elseif i == 2 then
						FDS.teamPoints['blue']['Players'][gpPN] = 0
					end
					if FDS.playersCredits[FDS.trueCoalitionCode[gpCoa]][gpUcid] == nil then
						FDS.playersCredits[FDS.trueCoalitionCode[gpCoa]][gpUcid] = 0
					end
				elseif i == 2 then
					gp = k:getGroup()
					gpId = gp:getID()
					gpCoa = k:getCoalition()
					gpPN = k:getPlayerName()
					gpName = k:getName()
					gpUcid = FDS.retrieveUcid(gpPN,FDS.isName)
					local cleanCargo = false
					if k:getCategory() == 1 then
						for i,j in pairs(FDS.heliSlots) do
							if k:getDesc().typeName == i then
								cleanCargo = true
							end
						end
						if cleanCargo then
							FDS.cargoList[tostring(k:getName())] = {} 
							FDS.valuableList[tostring(k:getName())] = {} 
						end
					end
					local msg = {}
					msg.text = gpPN .. ', you can help your team by:\n\n - Attacking ground targets in enemy zones (AG mission)(See map or [radio]>[F10]>[Where to attack]).\n\n - Attacking the enemy air transports in enemy supply route (AA mission) (See map).\n\n - Rescuing point around the map with helicopters (Helo rescue mission).\n - Killing enemy players in the process is always a good idea!\n\n - Visit our website: "https://dcs.comicorama.com/" for server and players stats.\n - Join our Discord community at FDS Server (Link available in the briefing). \nAn explanation about this server is available on our youtube channel: "FDS Server - DCS".'
					msg.displayTime = 60
					msg.sound = 'Welcome.ogg'
					mist.scheduleFunction(missionCommands.addCommandForGroup,{gpId,'Current War Status',nil, FDS.warStatus, {gpId, gpCoa, gpPN}},timer.getTime()+FDS.wtime)
					mist.scheduleFunction(missionCommands.addCommandForGroup,{gpId,'Where to Attack',nil, FDS.whereStrike, {gpId, gpCoa, gpName}},timer.getTime()+FDS.wtime)
					mist.scheduleFunction(missionCommands.addCommandForGroup,{gpId,'Where to Defend',nil, FDS.whereDefend, {gpId, gpCoa, gpName}},timer.getTime()+FDS.wtime)
					mist.scheduleFunction(missionCommands.addCommandForGroup,{gpId,'Drop Zones',nil, FDS.whereDropZones, {gpId, gpCoa, gpName}},timer.getTime()+FDS.wtime)
					--mist.scheduleFunction(missionCommands.addCommandForGroup,{gpId,'JTAC Status',nil, FDS.jtacStatus, {gpId, gpCoa, gpName}},timer.getTime()+FDS.wtime)
					FDS.addCreditsOptions(gp)
					FDS.addJtacOption(gp)
					FDS.addTroopManagement(gp)
					mist.scheduleFunction(trigger.action.outTextForGroup,{gpId,msg.text,msg.displayTime},timer.getTime()+FDS.wtime)
					mist.scheduleFunction(trigger.action.outSoundForGroup,{gpId,msg.sound},timer.getTime()+FDS.wtime)
					if i == 1 then 
						FDS.teamPoints['red']['Players'][gpPN] = 0
					elseif i == 2 then
						FDS.teamPoints['blue']['Players'][gpPN] = 0
					end
					if FDS.playersCredits[FDS.trueCoalitionCode[gpCoa]][gpUcid] == nil then
						FDS.playersCredits[FDS.trueCoalitionCode[gpCoa]][gpUcid] = 0
					end
				end
			end
		end
	end
	

	staticTypes = {}
	staticTypes.types = {'.Command Center','Shelter','Fuel tank'}
	staticTypes.number = {['.Command Center']= {nCP}, ['Shelter']={nHangarr,nHangarc}, ['Fuel tank'] = {nFuelr,nFuelc}}
	staticTypes.cat = {['.Command Center']= {4}, ['Shelter']={4}, ['Fuel tank'] = {4}}
	staticTypes.dist = {['.Command Center']= {deviation0, angle0}, ['Shelter']={{deviationHangarr, angleHangarr},{deviationHangarc, angleHangarc}}, ['Fuel tank'] = {{deviationFuelr, angleFuelr},{deviationFuelc, angleFuelc}}}
	staticTypes.collum = {['.Command Center']= {nCP}, ['Shelter']={nHangarr, nHangarc}, ['Fuel tank'] = {nFuelr, nFuelc}}

	for tz,cc in pairs(FDS.joinedZones) do
		zonePoint = zones[tz]["point"]
		addPoint = {x = zonePoint["x"],y = land.getHeight({x = zonePoint["x"], y = zonePoint["z"]}), z = zonePoint["z"]}

        -- Static Objects
		for j,i in pairs(staticTypes.types) do
			if i == '.Command Center' then
				addPoint = {x = addPoint["x"]+staticTypes.dist[i][1]*math.cos(staticTypes.dist[i][2]),y = land.getHeight({x = addPoint["x"]+staticTypes.dist[i][1]*math.cos(staticTypes.dist[i][2]), y = addPoint["z"]+staticTypes.dist[i][1]*math.sin(staticTypes.dist[i][2])}), z = addPoint["z"]+staticTypes.dist[i][1]*math.sin(staticTypes.dist[i][2])}
				height = land.getHeight({x = zonePoint["x"],y = zonePoint["z"]})

				addO = {}
				addO.country = cc
				addO.category = staticTypes.cat[i][1]
				addO.x = addPoint["x"]
				addO.y = addPoint["z"]
				addO.type = i
				addO.heading = haeding4All

				addCP = mist.dynAddStatic(addO)
				boxPos = {}
				for vert = 0,3,1 do 
					table.insert(boxPos,{x=addCP.x+40.0*math.cos(mist.utils.toRadian(addCP.heading+45.0+90.0*vert)), y=addCP.y+40.0*math.sin(addCP.heading+45.0+90.0*vert)})
				end
                if cc == 1 then
                    table.insert(tgtObj.blue[tz],{addCP.name,{x = addCP.x, y = addCP.y},boxPos,StaticObject.getByName(addCP.name):getCategory()})
                else
                    table.insert(tgtObj.red[tz],{addCP.name,{x = addCP.x, y = addCP.y},boxPos,StaticObject.getByName(addCP.name):getCategory()})
                end

			else
				for r = 0, staticTypes.collum[i][1]-1,1 do
					for c = 0, staticTypes.collum[i][2]-1,1 do 
						addingX = (r+1)*(staticTypes.dist[i][1][1]*math.cos(staticTypes.dist[i][1][2]))+c*(staticTypes.dist[i][2][1]*math.cos(staticTypes.dist[i][2][2]))
						addingY = (r+1)*(staticTypes.dist[i][1][1]*math.sin(staticTypes.dist[i][1][2]))+c*(staticTypes.dist[i][2][1]*math.sin(staticTypes.dist[i][2][2]))
						addPoint2 = {x = addPoint["x"]+addingX,y = land.getHeight({x = addPoint["x"]+addingX, y = addPoint["z"]+addingY}), z = addPoint["z"]+addingY}

						height = land.getHeight({x = zonePoint["x"],y = zonePoint["z"]})

						addO = {}
						addO.country = cc
						addO.category = staticTypes.cat[i][1]
						addO.x = addPoint2["x"]
						addO.y = addPoint2["z"]
						addO.type = i
						addO.heading = haeding4All

						addCP = mist.dynAddStatic(addO)
                        boxPos = {}
                        for vert = 0,3,1 do 
                            table.insert(boxPos,{x=addCP.x+80.0*math.cos(mist.utils.toRadian(addCP.heading+45.0+90.0*vert)), y=addCP.y+80.0*math.sin(addCP.heading+45.0+90.0*vert)})
                        end
                        if cc == 1 then
							table.insert(tgtObj.blue[tz],{addCP.name,{x = addCP.x, y = addCP.y},boxPos,StaticObject.getByName(addCP.name):getCategory()})
                        else
                            table.insert(tgtObj.red[tz],{addCP.name,{x = addCP.x, y = addCP.y},boxPos,StaticObject.getByName(addCP.name):getCategory()})
                        end
					end
				end
			end
		end
        -- Ground Units
        for unc, qt in pairs(FDS.tgtQty) do
            for unitNumber = 0,qt[1],1 do
				if unitNumber ~= 0 then
					checkP = true
					it = 0
					while checkP==true do
						bornPoint = mist.getRandomPointInZone(tz)
						if cc == 1 then
							for nObj, cObj in ipairs(tgtObj.blue[tz]) do
								checkP = mist.pointInPolygon(bornPoint,cObj[3])
							end
						else
							for nObj, cObj in ipairs(tgtObj.red[tz]) do
								checkP = mist.pointInPolygon(bornPoint,cObj[3])
							end
						end
						it = it + 1
						if it > 10 then
							checkP = false
						end
					end
					addUnit = {}
					local mockName = ''
					if cc == 1 then
						mockName = 'Blue_' .. qt[2]
					else
						mockName = 'Red_' .. qt[2]
					end
					-- Strap
					local gp = Group.getByName(mockName)
					local gPData = mist.getGroupData(mockName,true)
					local gpR = mist.getGroupRoute(gp:getName(),true)
					local addUnit_gp = mist.utils.deepCopy(gpR)
					local addUnit = mist.utils.deepCopy(gPData)
					--
					--addUnit.x = bornPoint.x
					--addUnit.y = bornPoint.y
					--addUnit.type = unc
					--addUnit.skill = 'Ace'
					--addUnit.heading = math.random(0.0,359.0)

					--allUnits = {}
					--table.insert(allUnits,addUnit)

					addO = addUnit
					--addO = {}
					--addO.units = allUnits
					addO.country = cc
					addO.category = 2
					addO.visible = true
					addO.clone = true
					addO.units[1].x = bornPoint.x
					addO.units[1].y = bornPoint.y
					addO.units[1].heading =  math.random(0.0,359.0)
					addUni = mist.dynAdd(addO)

					boxPos = {}
					for vert = 0,3,1 do 
						table.insert(boxPos,{x=addUni.units[1].x+40.0*math.cos(mist.utils.toRadian(addUni.units[1].heading+45.0+90.0*vert)), y=addUni.units[1].y+40.0*math.sin(addUni.units[1].heading+45.0+90.0*vert)})
					end
					FDS.entityKills[addUni.name] = nil
					FDS.killedByEntity[addUni.name] = nil
					if cc == 1 then
						table.insert(tgtObj.blue[tz],{addUni.name,{x = addUni.units[1].x, y = addUni.units[1].y},boxPos,Group.getByName(addUni.name):getCategory()})
					else
						table.insert(tgtObj.red[tz],{addUni.name,{x = addUni.units[1].x, y = addUni.units[1].y},boxPos,Group.getByName(addUni.name):getCategory()})
					end
				end
            end
        end
		-- Data export Vector for all units in zone
		FDS.initTgtObj = mist.utils.deepCopy(tgtObj)
		for _,i in pairs(FDS.initTgtObj) do
			for _, j in pairs(i) do
				for _, k in pairs(j) do
					if StaticObject.getByName(k[1]) then
					   k[5] = StaticObject.getByName(k[1]):getDesc().typeName
					else
					   k[5] = Group.getByName(k[1]):getUnit(1):getDesc().typeName
					end
				end  
			end
		end
	end
	-- Data to sent to redis
	local redisString = {}
	for coalition, zone in pairs(FDS.initTgtObj) do
		for zoneName, unitName in pairs(zone) do
			local iter = 1
			redisStringAdd = tostring(zoneName)
			redisStringAdd = {redisStringAdd:gsub("%s", "")}
			redisStringAdd = {'idTablesZones:'..redisStringAdd[1]}
			for _, set in pairs(unitName) do
				local gpId = StaticObject.getByName(set[1]) or Group.getByName(set[1])
				if gpId:getCategory() ~= 3 then
					gpId = gpId:getUnits()[1].id_
				else
					gpId = gpId.id_
				end
				table.insert(redisStringAdd, tostring(iter))
				table.insert(redisStringAdd, tostring(gpId))
				iter = iter + 1
			end
			table.insert(redisString, redisStringAdd)
		end
	end
	if DFDS ~= nil then
		local replies = DFDS.client:pipeline(function(p)
			for _, values in pairs(redisString) do
				p:hset(values)
			end
		end)
	end
end 
'''