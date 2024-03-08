import cmd
import sys
import json
import grpc
import serviceConn_pb2_grpc as p2p_pb2_grpc
import serviceConn_pb2 as p2p_pb2
from pclient import P2PClient
from pserver import P2PServer


class ClientConsole(cmd.Cmd):
    intro = 'Welcome to the P2P file sharing system. Type help or ? to list commands.\n'
    prompt = '(P2P) '

    def __init__(self, config_file):
        super().__init__()
        self.config = self.load_config(config_file)
        self.channel = grpc.insecure_channel(self.config['grpc_server'])
        self.stub = p2p_pb2_grpc.P2PServiceConnectionStub(self.channel)
        self.bootstrap()

    def load_config(self, config_file):
        """Load configuration from file"""
        with open(config_file, 'r') as file:
            return json.load(file)

    def do_handshake(self, args):
        """Realiza el handshake con el servidor o un peer."""
        P2PClient.handshakeFunc(self, self.config['peer_info'])

    def do_discover_peers(self, args):
        """Descubre peers en la red."""
        try:
            response = self.stub.GetPeers(p2p_pb2.Empty())
            for peer in response.peers:
                print(f"Peer descubierto: {peer.peer_id} en {peer.ip}:{peer.port}")
        except grpc.RpcError as e:
            print(f"Error al descubrir peers: {e.details()}")

    def bootstrap(self):
        """Inicializa el cliente realizando el handshake y descubriendo peers."""
        self.do_handshake(None)
        self.do_discover_peers(None)

    def do_start(self, args):
        """Start a peer server. Usage: start [ip] [port]"""
        if not args:
            print("Usage: start <ip> <port>")
            return
        try:
            ip, port = args.split()
            self.peer_manager.start_listener(ip, int(port))
            print(f"Server started on {ip}:{port}")
        except ValueError:
            print("Usage: start <ip> <port>")

    def do_connect(self, args):
        """Connect to a specific peer server. Usage: connect [ip] [port]"""
        if not args:
            print("Usage: connect <ip> <port>")
            return
        try:
            ip, port = args.split()
            peer_socket = self.connect_to_peer(ip, int(port))
            if peer_socket:
                self.connected_peer = (ip, port, peer_socket)
                print(f"Connected to {ip}:{port} successfully.")
            else:
                print(f"Failed to connect to {ip}:{port}")
        except ValueError:
            print("Usage: connect <ip> <port>")

    def do_list_peers(self, args):
        """List active peers. Usage: listpeers"""
        active_peers = self.peer_manager.get_active_peers()
        for peer in active_peers:
            print(f"Active peer: {peer}")

    def do_list_files(self, args):
        """List files available on the connected peer. Usage: <listfiles>"""
        self.log("List files command executed")
        self.log("Listing available files...")

        # List of files available

        self.log("Files listed successfully.")

    def do_download(self, args):
        """Download a file from the connected peer. Usage: download <filename>"""
        if not args:
            self.log("Usage: download <filename>", "ERROR")
            return
        filename = args.strip()
        self.log(f"Download command executed")

        # Downloading a file
        self.log(f"Downloading file: {filename}...")

    def do_upload(self, args):
        """Upload a file to the connected peer. Usage: upload <filename>"""
        if not args:
            self.log("Usage: upload <filename>", "ERROR")
            return
        filename = args.strip()
        self.log(f"Upload command executed")

        # Uploading a file
        self.log(f"Downloading file: {filename}...")

    def do_exit(self, _):
        """Exit the application. Usage: exit"""
        print("Exiting the application...")
        return True  


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <config_file>")
        sys.exit(1)
    config_file = sys.argv[1]
    ClientConsole(config_file).cmdloop()