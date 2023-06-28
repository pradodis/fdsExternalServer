import grpc
import time

# Import the generated gRPC classes

from binds import custom_pb2
from binds import custom_pb2_grpc

class internalLuaLink:
    def __init__(self, server_address, server_port):
        self.channel = grpc.insecure_channel(f'{server_address}:{server_port}')
        self.stub = custom_pb2_grpc.CustomServiceStub(self.channel) 

    def send(self, code):
        start = time.time()
        try:
            # Make a gRPC request
            request = custom_pb2.EvalRequest()
            request.lua = code

            # Call the gRPC method
            response = self.stub.Eval(request)

            # Print the response
            end = time.time()
            print("Internal LUA Feedback: " + str(response) + " - Elapsed Time: " + str(end - start) + "s\n")
             
        except grpc.RpcError as e:
            print(f'Error: {e}')