import grpc
import json
from . import commonDictionaries as cd

# Import the generated gRPC classes

from dcs.mission.v0 import mission_pb2
from dcs.mission.v0 import mission_pb2_grpc

def birth_response(response, commomGD, live_units):
    commomGD.onLinePlayersCheck()
    player_name = commomGD.onLinePlayers["unit"][response.birth.initiator.unknown.name]["playerName"]
    unit_type = commomGD.onLinePlayers["unit"][response.birth.initiator.unknown.name]["type"]
    live_units.fetch()
    print(cd.bcolors.PURPLE + '---> ' + player_name + ' CONTROLS: ' + unit_type + cd.bcolors.ENDC)

# PLAYER LEAVE UNIT
def player_leave_unit_response(response, commomGD):
    player_name = commomGD.onLinePlayers["unit"][response.player_leave_unit.initiator.unknown.name]["playerName"]
    unit_type = commomGD.onLinePlayers["unit"][response.player_leave_unit.initiator.unknown.name]["type"]
    print(cd.bcolors.PURPLE + '---> ' + player_name + ' LEFT: ' + unit_type + cd.bcolors.ENDC)
    commomGD.onLinePlayersCheck()

# MISSION END
def mission_end_response(redis_object):
    redis_object.set("ongoing_zoneassault", "False")

# KILL
def kill_response(response, live_units):
    if response.kill.initiator.unknown.name in live_units.liveUnits and response.kill.target.unknown.name in live_units.liveUnits:
        color = ''
        if live_units.liveUnits[response.kill.initiator.unknown.name]["coalition"] == 'blue': 
            color = cd.bcolors.BLUE; 
        elif live_units.liveUnits[response.kill.initiator.unknown.name]["coalition"] == 'red': 
            color = cd.bcolors.RED
        print(color + '---> ' + response.kill.initiator.unknown.name + ' KILLED: ' + response.kill.target.unknown.name + cd.bcolors.ENDC)

class eventFetcher:
    def __init__(self, server_address, server_port, **kwargs):
        self.channel = grpc.insecure_channel(f'{server_address}:{server_port}')
        self.stub = mission_pb2_grpc.MissionServiceStub(self.channel)
        self.response = []
        self.commomGD = kwargs["commom_game_data"]
        self.r = kwargs["redis_conn"]
        self.live_units = kwargs["live_units"]
        print("\033[92m" + "EVENT FETCHER INITIALIZED" + "\033[0m")

    def fetch(self):
        try:
            request = mission_pb2.StreamEventsRequest()
            self.response = self.stub.StreamEvents(request)
            print("Events Stream Initiated")
        except grpc.RpcError as e:
            print(f'Error: {e}')

    def evaluateEvents(self):
        processed_event = {}  # Conjunto para armazenar identificadores de eventos processados
        try: 
            for event in self.response:
                event_id = event
                # EVENT HANDLER
                if self.event_loop(event_id, processed_event):
                    if event.HasField("player_leave_unit"): 
                        player_leave_unit_response(event, self.commomGD)
                    elif event.HasField("birth"):
                        birth_response(event, self.commomGD, self.live_units)
                    elif event.HasField("kill"):
                        print(event)
                        kill_response(event, self.live_units)
                    elif event.HasField("mission_end"):
                        mission_end_response(self.r)
                    processed_event = event_id
                else:
                    #print(f"Evento duplicado (ID: {event_id}). Fim de stream.")
                    break
        except StopIteration:
            print("Todos os eventos da stream foram processados.")
        except Exception as e:
            print(f"Um erro ocorreu ao processar os eventos: {e}")
    
    def event_loop(self, current_event, previous_event):
        if previous_event != {} and previous_event.time > current_event.time - 1.5:
            if previous_event.HasField("simulation_fps") and current_event.HasField("simulation_fps"):
                return False
            else:
                return True
        else:
            return True
