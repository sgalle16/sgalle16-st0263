package main

import (
	"flag"
	"fmt"
	"log"
	"net"

	"github.com/sgalle16/sgalle16-st0263/P2PFileSharingSystem/server/p2p"
	pb "github.com/sgalle16/sgalle16-st0263/P2PFileSharingSystem/server/proto"
	"google.golang.org/grpc"
)

var port_bp_1 = flag.Int("port", 50056, "Bootstrap Peer by default port to connect to")

func main() {
	flag.Parse()
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", *port_bp_1))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	P2PServer := p2p.NewP2PServer()
	pb.RegisterP2PServiceConnectionServer(s, P2PServer)
	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
