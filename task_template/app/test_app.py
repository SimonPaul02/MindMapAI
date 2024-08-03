import grpc.aio as grpc
import grpc_server., tangram_pb2_grpc

channel = grpc.insecure_channel(f"localhost:8061")
stub = tangram_pb2_grpc.ServiceStarterStub(channel)
request = tangram_pb2.Empty()
response = stub.startService(request)
print("done")
