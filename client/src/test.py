import grpc
import logging
import serviceConn_pb2
import serviceConn_pb2_grpc

def run_handshake():
    # config default
    server_ip = "localhost"  # default ip 
    server_port = "55555"       
    
    # logging
    logging.basicConfig(level=logging.INFO)
    
    #  canal y stub para comunicarse con el server gprc
    channel = grpc.insecure_channel(f'{server_ip}:{server_port}')
    stub = serviceConn_pb2_grpc.P2PServiceConnectionStub(channel)
    
    try:
        # enviar solicitud de handshake
        response = stub.Handshake(serviceConn_pb2.HandshakeRequest(
            peerInfo=serviceConn_pb2.PeerInfo(
                peer_id="client_test",
                ip=server_ip,
                port=int(server_port))
        ))
        
        #verificar la respuesta del server
        if response.success:
            logging.info(f"Handshake successful. Message: {response.message}")
        else:
            logging.info("Handshake failed. Server responded with failure.")
    except grpc.RpcError as e:
        logging.error(f"Failed to connect to server at {server_ip}:{server_port}, error: {e}")

if __name__ == '__main__':
    run_handshake()
