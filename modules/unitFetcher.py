import grpc
import time
import logging
import ipaddress
from . import commonDictionaries as cd
from dcs.mission.v0 import mission_pb2
from dcs.mission.v0 import mission_pb2_grpc

class UnitFetcherError(Exception):
    """Custom exception for UnitFetcher errors"""
    pass

class unitFetcher:
    def __init__(self, server_address, server_port):
        # Validate inputs
        try:
            ipaddress.ip_address(server_address)
            if not 1 <= server_port <= 65535:
                raise ValueError("Port must be between 1 and 65535")
        except ValueError as e:
            raise UnitFetcherError(f"Invalid address or port: {e}")

        # Set up secure channel with SSL/TLS (recommended)
        try:
            credentials = grpc.ssl_channel_credentials()
            self.channel = grpc.secure_channel(
                f'{server_address}:{server_port}',
                credentials
            )
        except Exception:
            logging.warning("Falling back to insecure channel")
            self.channel = grpc.insecure_channel(f'{server_address}:{server_port}')
            
        self.stub = mission_pb2_grpc.MissionServiceStub(self.channel)
        self.liveUnits = {}
        self.response = []
        logging.info("Live units fetcher initialized")

    def fetch(self):
        try:
            self.request = mission_pb2.StreamUnitsRequest()
            self.request.poll_rate = 1
            self.request.max_backoff = 10
            self.request.category = "GROUP_CATEGORY_UNSPECIFIED"
            self.response = self.stub.StreamUnits(self.request)
            logging.info("Unit stream initiated")
        except grpc.RpcError as e:
            logging.error("Stream error occurred")
            raise UnitFetcherError("Failed to fetch units") from e

    def listUnits(self):
        processed_events = set()
        try:
            for newEvent in self.response:
                event_id = newEvent.unit.name
                if not newEvent.gone.name:
                    if event_id not in processed_events:
                        dataDict = {
                            "oid": newEvent.unit.oid,
                            "id": newEvent.unit.id,
                            "name": newEvent.unit.name,
                            "coalition": cd.coalition_code_network[str(newEvent.unit.coalition)],
                            "position": {
                                "u": newEvent.unit.position.u,
                                "v": newEvent.unit.position.v
                            },
                            "orientation": {
                                "heading": newEvent.unit.position.u,
                                "yaw": newEvent.unit.position.v, 
                                "pitch": newEvent.unit.position.v,
                                "roll": newEvent.unit.position.v
                            },
                            "type": newEvent.unit.type,
                            "category": cd.grpc_object_category[str(newEvent.unit.group.category)]
                        }
                        logging.debug("Unit data updated: %s", event_id)
                        self.liveUnits[newEvent.unit.name] = dataDict
                        processed_events.add(event_id)
                    else:
                        break
                else:
                    self.liveUnits[newEvent.gone.name] = {}
        except StopIteration:
            logging.info("Stream processing complete")
        except Exception as e:
            logging.error("Error processing units: %s", str(e))
            raise UnitFetcherError("Failed to process units") from e