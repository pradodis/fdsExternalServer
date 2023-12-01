import grpc
import time

# Import the generated gRPC classes

from dcs.mission.v0 import mission_pb2
from dcs.mission.v0 import mission_pb2_grpc

class unitFetcher:
    def __init__(self, server_address, server_port):
        self.channel = grpc.insecure_channel(f'{server_address}:{server_port}')
        self.stub = mission_pb2_grpc.MissionServiceStub(self.channel)
        self.liveUnits = []
        print("\033[92m" + "LIVE UNITS FETCHER INITIALIZED" + "\033[0m")

    def fetch(self):
        try:
            request = mission_pb2.StreamUnitsRequest()
            response = self.stub.StreamUnits(request)
            self.liveUnits = response
            print("Unit Stream Initiated")
        except grpc.RpcError as e:
            print(f'Error: {e}')