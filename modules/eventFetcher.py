import grpc
import json

# Import the generated gRPC classes

from dcs.mission.v0 import mission_pb2
from dcs.mission.v0 import mission_pb2_grpc

class eventFetcher:
    def __init__(self, server_address, server_port, **kwargs):
        self.channel = grpc.insecure_channel(f'{server_address}:{server_port}')
        self.stub = mission_pb2_grpc.MissionServiceStub(self.channel)
        self.response = []
        self.commomGD = kwargs["commom_game_data"]
        print("\033[92m" + "EVENT FETCHER INITIALIZED" + "\033[0m")

    def fetch(self):
        try:
            request = mission_pb2.StreamEventsRequest()
            self.response = self.stub.StreamEvents(request)
            print("Events Stream Initiated")
        except grpc.RpcError as e:
            print(f'Error: {e}')

    def evaluateEvents(self):
        futures = []
        futures.append(self.response)
        for event in futures:
#            try:
            repeat = True
            while repeat:
                newEvent = event.next()
                # EVENT HANDLER
                # PLAYER LEAVE UNIT
                if not newEvent.HasField("simulation_fps") and not newEvent.HasField("weapon_add"):
                    print(newEvent)
                    if newEvent.HasField("player_leave_unit"): 
                        print(newEvent.player_leave_unit.initiator.unit)
                    elif newEvent.HasField("player_change_slot"):
                        self.commomGD.onLinePlayersCheck()