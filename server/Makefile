build:
	@go build -o bin/server

run: build
	@./bin/server

test:
	@go test ./... -v

proto:
	protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    proto/serviceConn.proto

.PHONY: proto