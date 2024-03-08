from concurrent import futures
import json
import threading
import grpc
import serviceConn_pb2_grpc as p2p_pb2_grpc
import serviceConn_pb2 as p2p_pb2
from pclient import P2PClient


class P2PServer(p2p_pb2_grpc.P2PServiceConnectionServicer):

    def __init__(self, config_file="config.json"):

        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file) as f:
            return json.load(f)


def serve(server_port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    p2p_pb2_grpc.add_P2PServiceConnectionServicer_to_server(
        P2PServer(), server)
    server.add_insecure_port(server_port)
    server.start()
    print(f"Server listening on {server_port}")
    server.wait_for_termination()
