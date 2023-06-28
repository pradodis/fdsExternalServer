import grpc
import time

# Import the generated gRPC classes

from binds import mission_pb2
from binds import mission_pb2_grpc

class eventFetcher:
    def __init__(self, server_address, server_port):
        self.channel = grpc.insecure_channel(f'{server_address}:{server_port}')
        self.stub = mission_pb2_grpc.MissionServiceStub(self.channel)
        self.currentEvents = []
        
    def fetch(self):
        start = time.time()
        try:
            # Make a gRPC request
            request = mission_pb2.StreamEventsRequest()

            # Call the gRPC method
            response = self.stub.StreamEvents(request)

            # Print the response
            self.currentEvents = response
            end = time.time()
            print("Events Refreshed - Elapsed time: " + str(end - start) + "s\n")

        except grpc.RpcError as e:
            print(f'Error: {e}')