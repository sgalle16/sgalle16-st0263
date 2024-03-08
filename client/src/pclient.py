import json
import logging
import threading
import grpc
import serviceConn_pb2_grpc as p2p_pb2_grpc
import serviceConn_pb2 as p2p_pb2
import pserver
from utils import get_local_ip


class P2PClient(p2p_pb2_grpc.P2PServiceConnectionServicer):

    def __init__(self, config_file):

        self.config = self.load_config(config_file)
        # lista de peers conocidos o bootstrap peers
        self.bootstrap_peers = self.config.get('bootstrap_peers', [])
        # los peers conocidos......
        self.known_peers = self.config.get('known_peers', [])

        self.active_peers = []

    # Attempt - Handshake connection between peers

    def load_config(self, config_file):
        with open(config_file) as f:
            return json.load(f)


# intenta establecer una conexión con el peer especificado y devuelve True si la conexión es exitosa,
# False si falla o no puede determinar si la conexión fue exitosa o no.


    def handshakeFunc(self, peer_info):

        ip, port = self.get_ip_and_port(peer_info)
        channel = grpc.insecure_channel(f'{ip}:{port}')
        stub = p2p_pb2_grpc.P2PServiceConnectionStub(channel)

        try:

            response = stub.Handshake(p2p_pb2.HandshakeRequest(
                peerInfo=p2p_pb2.PeerInfo(
                    peer_id=peer_info['peer_id'],
                    ip=peer_info['listening_ip'],
                    port=peer_info['listening_port'])
            )
            )
            if response.success:
                logging.info(
                    f"Handshake successful with {ip}:{port}, Message: {response.message}")
                # Monitorear las conexiones de los peers en segundo plano
                self.monitor_peers_in_background(stub, peer_info['peer_id'])  #
                return stub  # para que se pueda usar en otras conexiones
            else:
                logging.error(f"Handshake failed with {ip}:{port}")
                return None
        except grpc.RpcError as e:
            logging.warning(
                f"Failed to connect to {ip}:{port}, error: {str(e)}")
            return None

    def get_and_connect_to_peers(self, stub, peer_info):

        ip, port = self.get_ip_and_port(peer_info)
        # Obtiene la lista de peers después del handshake exitoso
        # Conecta con los peers obtenidos
        try:
            response = stub.GetPeers(p2p_pb2.Empty())
            for peer in response.peers:
                print(f"Retrying to connect to: {peer.peer_id} en {peer.ip}:{peer.port}")

                if peer.peer_id not in [p['peer_id'] for p in self.known_peers]:
                        self.handshakeFunc({'peer_id': peer.peer_id, 'listening_ip': peer.ip, 'listening_port': peer.port})
        except grpc.RpcError as e:
            logging.error(f"Failed to get and connect to peers: {str(e)}")


    # Intenta conectarse a los bootstrap peers en orden hasta que uno de ellos responda.

    def try_connect_bootstrap(self, peer_info):  # Añade peer_info como argumento
        ip, port = self.get_ip_and_port(peer_info)
        channel = grpc.insecure_channel(f"{ip}:{port}")
        stub = p2p_pb2_grpc.P2PServiceConnectionStub(channel)
        response = stub.Handshake(p2p_pb2.HandshakeRequest(
            peerInfo=p2p_pb2.PeerInfo(
                peer_id=peer_info['peer_id'],
                ip=peer_info['listening_ip'],
                port=peer_info['listening_port'])
        ))
        if response.success:
            logging.info(
                f"Handshake successful with {ip}:{port}, Message: {response.message}")
            return stub  # Devuelve el stub si la conexión es exitosa
        else:
            # ...
            return None  # Devuelve None si la conexión no es exitosa

    # GetPeers

    def get_peers(self, stub, peer_info):
        try:
            response = stub.GetPeers(p2p_pb2.Empty())
            print(response.peers)
            return response.peers
        except grpc.RpcError as e:
            print(
                f"Failed to get peers from {peer_info['listening_ip']}:{peer_info['listening_port']}, error: {e}")
            return []

    # el peer actual actua empieza a actuar como servidor en {50500}

    def run_as_server(self):
        server_port = f"{get_local_ip()}:{50500}"
        threading.Thread(target=lambda: pserver.serve(
            server_port), daemon=True).start()
        logging.info(f"Acting as server on {server_port}")
        input()


# después de establecer una conexión con un peer o con el bootstrap peer,
# inicia un hilo separado para monitorear los peers conectados y actualizar la lista de peers.

    def monitor_peers_in_background(self, stub, peer_id):
        def peer_status_updates():
            yield p2p_pb2.PeerStatusUpdate(peer_id=peer_id, online=True)
        thread = threading.Thread(target=self.monitor_peers, args=(stub, peer_id))
        thread.daemon = True
        thread.start()

    def monitor_peers(self, stub, peer_id):

        try:
            responses = stub.MonitorPeers(
                p2p_pb2.PeerStatusUpdate(peer_id=peer_id, online=True))
            for response in responses:
                print("Update from server:", response.message)
                if response.success:
                    # Update the known_peers list
                    self.known_peers = [
                        peer for peer in self.known_peers if peer['peer_id'] != response.peer_id]
                    if response.online:
                        self.active_peers.append(
                            {'peer_id': response.peer_id, 'listening_ip': response.ip, 'listening_port': response.port})
                else:
                    print(f"Peer {response.peer_id} disconnected.")
        except grpc.RpcError as e:
            print(f"Stream closed by server with error: {e}")

    def process_peer_update(self, update):
        if update.online and update.peer_id not in [peer['peer_id'] for peer in self.known_peers]:
            self.known_peers.append(
                {'peer_id': update.peer_id, 'listening_ip': update.ip, 'listening_port': update.port})
            logging.info(f"New peer added: {update.peer_id}")
        elif not update.online:
            self.known_peers = [
                peer for peer in self.known_peers if peer['peer_id'] != update.peer_id]
            logging.info(f"Peer removed: {update.peer_id}")

    # Discovery Service ...
    """def discover_peers(self):
        pass

    def discover_resources(self, resource_id):
        pass

    def send_discovery_message(self, peer_info):
        pass

    def send_message(self, peer_info, message):
        pass"""

    @staticmethod
    def get_ip_and_port(peer_info):
        if isinstance(peer_info, dict):
            # Acceso como diccionario
            ip = peer_info["listening_ip"]
            port = peer_info["listening_port"]
        else:
            # Acceso como objeto PeerInfo
            ip = peer_info.ip
            port = peer_info.port
        return ip, port

    def get_stub(self, peer_info):
        channel = grpc.insecure_channel(
            f"{peer_info['listening_ip']}:{peer_info['listening_port']}")
        return p2p_pb2_grpc.P2PServiceConnectionStub(channel)

    def run(self):
        all_peers = self.bootstrap_peers + self.known_peers
        for peer_info in all_peers:
            stub = self.try_connect_bootstrap(peer_info)
            if stub is not None:
                logging.info("Connected to bootstrap peer.")
                
                self.get_and_connect_to_peers(stub, peer_info)
                break
            elif self.handshakeFunc(peer_info):
                print(f"Connected to peer {peer_info['peer_id']}.")
                
                peer_stub = self.get_stub(peer_info)
                self.get_and_connect_to_peers(peer_stub, peer_info)
            else:
                print(f"Failed to connect to peer {peer_info['peer_id']}.")
                # acting as server
                self.run_as_server()
                break


if __name__ == '__main__':
    client = P2PClient("config.json")
    client.run()
