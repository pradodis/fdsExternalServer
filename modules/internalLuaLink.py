import grpc
import time

# Import the generated gRPC classes

from dcs.custom.v0 import custom_pb2
from dcs.custom.v0 import custom_pb2_grpc

class internalLuaLink:
    def __init__(self, server_address, server_port):
        self.channel = grpc.insecure_channel(f'{server_address}:{server_port}')
        self.stub = custom_pb2_grpc.CustomServiceStub(self.channel)
        print("\033[92m" + "INTERNAL LUA LINK INITIALIZED" + "\033[0m")

    def send(self, code):
        try:
            # Make a gRPC request
            request = custom_pb2.EvalRequest()
            request.lua = code
            # Call the gRPC method
            response = self.stub.Eval(request)
            return response

        except grpc.RpcError as e:
            print(f'Error: {e}')