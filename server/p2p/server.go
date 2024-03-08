package p2p

import (
	"context"
	"fmt"
	"io"
	"log"
	"sync"

	pb "github.com/sgalle16/sgalle16-st0263/P2PFileSharingSystem/server/proto"
)

// P2PServer is a server that handles P2P connections.
type P2PServer struct {
	pb.UnimplementedP2PServiceConnectionServer

	mu    sync.Mutex  
	peers map[string]*pb.PeerInfo 
	peerLists map[string][]*pb.PeerInfo 
}

// NewP2PServer creates a new P2P server.
func NewP2PServer() *P2PServer {
	return &P2PServer{
		peers: make(map[string]*pb.PeerInfo),
		peerLists: make(map[string][]*pb.PeerInfo),
	}

}

// Handshake performs a handshake with a peer.
// It receives a HandshakeRequest containing peer information and adds the peer to the server's list of peers.
// The function returns a HandshakeResponse indicating the success of the handshake.
func (s *P2PServer) Handshake(ctx context.Context, req *pb.HandshakeRequest) (*pb.HandshakeResponse, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	peerInfo := req.GetPeerInfo()
	s.peers[peerInfo.GetPeerId()] = peerInfo
	for _, peerInfo := range s.peerLists[peerInfo.GetPeerId()] {
		s.peerLists[peerInfo.GetPeerId()] = append(s.peerLists[peerInfo.GetPeerId()], peerInfo)
	}
	log.Printf("Handshake received from %s\n", peerInfo.String())

	return &pb.HandshakeResponse{Success: true, Message: "Handshake successful.%s Welcome to the P2P Network!"}, nil
}

// Global variable to keep track of all connected peers for broadcasting updates
var (
	peerConnections   = make(map[string]pb.P2PServiceConnection_MonitorPeersServer)
	peerConnectionsRW sync.RWMutex
)

// MonitorPeers monitors the status of connected peers.
func (s *P2PServer) MonitorPeers(stream pb.P2PServiceConnection_MonitorPeersServer) error {
    initialPeerStatus, err := stream.Recv()
    if err != nil {
        log.Printf("Failed to receive initial status from peer: %v", err)
        return err
    }
    peerID := initialPeerStatus.PeerId
    fmt.Printf("Peer %s connected.\n", peerID)

    peerConnectionsRW.Lock()
    peerConnections[peerID] = stream
    peerConnectionsRW.Unlock()

    // Broadcast the new peer's status to all other peers
    broadcastPeerStatus(initialPeerStatus)

    for {
        peerStatus, err := stream.Recv()
        if err == io.EOF {
            fmt.Printf("Peer %s disconnected.\n", peerID)
            deletePeerConnection(peerID)
            broadcastPeerStatus(&pb.PeerStatusUpdate{
                PeerId: peerID,
                Online: false,
            })
            break
        }
        if err != nil {
            log.Printf("Failed to receive status update from peer %s: %v", peerID, err)
            deletePeerConnection(peerID)
            return err
        }
        broadcastPeerStatus(peerStatus)
    }

    return nil
}

func deletePeerConnection(peerID string) {
	peerConnectionsRW.Lock()
	defer peerConnectionsRW.Unlock()
	if stream, ok := peerConnections[peerID]; ok {
		err := stream.Send(&pb.PeerUpdateResponse{
			Success: false,
			Message: "Peer disconnected",
		})
		if err != nil {
			log.Printf("Failed to send update to peer %s: %v", peerID, err)
		}
		delete(peerConnections, peerID)
	}
}

func broadcastPeerStatus(status *pb.PeerStatusUpdate) {
    peerConnectionsRW.Unlock()
    defer peerConnectionsRW.RUnlock()
    for id, stream := range peerConnections {
        if id != status.PeerId {
            err := stream.Send(&pb.PeerUpdateResponse{
                Success: true,
                Message: fmt.Sprintf("Peer %s status updated: %v", status.PeerId, status.Online),
            })
            if err != nil {
                log.Printf("Failed to send update to peer %s: %v", id, err)
            }
        }
    }
}

// GetPeers returns a list of all connected peers.
func (s *P2PServer) GetPeers(ctx context.Context, empty *pb.Empty) (*pb.PeerList, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	var peers []*pb.PeerInfo
	for _, peerInfo := range s.peers {
		peers = append(peers, peerInfo)
	}
	return &pb.PeerList{Peers: peers}, nil
}
