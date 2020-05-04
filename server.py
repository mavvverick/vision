import grpc
from concurrent import futures
import nsfw
import logo
# import the generated classes
import dense_pb2
import dense_pb2_grpc
import time
import asyncio
from threading import current_thread

# https://github.com/comzyh/python-grpc-async-server-example/blob/master/server.py
# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. dense.proto


class DenseServicer(dense_pb2_grpc.PredictServicer):
    def predict_nsfw(self, request, context):
        post_id = request.postId
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(nsfw.http(post_id))
        print_thread(post_id)
        loop.close()
        return dense_pb2.Response(message="OK")

    def predict_logo(self, request, context):
        response = logo.http(request.postId)
        print(response)
        return dense_pb2.Response(message="OK")

    def predict_pipeline(self, request, context):
        post_id = request.postId
        # Download file here
        loop = asyncio.new_event_loop()
        proxy = loop.run_until_complete(task_manager(post_id))
        loop.close()
        print(proxy)
        print_thread(post_id)
        # CHECK for nsfw or watermark
        # return result
        return dense_pb2.Response(message="OK")


def print_thread(post_id):
    print("current_thread: {}, post: {}".format(
        current_thread().name, post_id))
    return


async def task_manager(post_id):
    t1 = asyncio.create_task(nsfw.http(post_id))
    t2 = asyncio.create_task(logo.http(post_id))
    tasks = [t1, t2]
    while tasks:
        finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for x in finished:
            result = x.result()
            # keep task counter, collerct results and retuen when all tasks ate finsihed
            if result:
                # check for result
                # cancel the other tasks, we have a result. We need to wait for the cancellations
                # to propagate.
                # for task in unfinished:
                #     task.cancel()
                # await asyncio.wait(unfinished)
                return result
        tasks = unfinished

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
