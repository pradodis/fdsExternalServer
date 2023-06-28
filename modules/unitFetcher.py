import grpc
import time

# Import the generated gRPC classes

from binds import mission_pb2
from binds import mission_pb2_grpc

class unitFetcher:
    def __init__(self, server_address, server_port):
        self.channel = grpc.insecure_channel(f'{server_address}:{server_port}')
        self.stub = mission_pb2_grpc.MissionServiceStub(self.channel)
        self.liveUnits = []

    def fetch(self):
        start = time.time()
        try:
            # Make a gRPC request
            request = mission_pb2.StreamUnitsRequest()

            # Call the gRPC method
            response = self.stub.StreamUnits(request)

            # Print the response
            self.liveUnits = response
            end = time.time()
            print("Units Refreshed - Elapsed time: " + str(end - start) + "s\n")

        except grpc.RpcError as e:
            print(f'Error: {e}')