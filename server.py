import grpc
from concurrent import futures
import nsfw
import logo
# import the generated classes
import dense_pb2
import dense_pb2_grpc
import time


# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. dense.proto
class DenseServicer(dense_pb2_grpc.PredictServicer):
    def predict_nsfw(self, request, context):
        response = nsfw.http(request.postId)
        print(response)
        return dense_pb2.Response(message="OK")

    def predict_logo(self, request, context):
        response = logo.http(request.postId)
        print(response)
        return dense_pb2.Response(message="OK")


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

dense_pb2_grpc.add_PredictServicer_to_server(
    DenseServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
