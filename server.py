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
from common import download_unzip, get_max_from_list_of_dict, GCSClient
import settings
import json

# https://github.com/comzyh/python-grpc-async-server-example/blob/master/server.py
# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. dense.proto


class DenseServicer(dense_pb2_grpc.PredictServicer):

    def __init__(self):
        self.gcs_client = GCSClient.Instance().storage_client

    def predict_nsfw(self, request, context):
        post_id = request.postId
        try:
            res = asyncio.run(nsfw.http(post_id))
            print(res)
        except Exception as e:
            print(e)
        print_thread(post_id)
        return dense_pb2.Response(message="OK")

    def predict_logo(self, request, context):
        try:
            response = asyncio.run(logo.http(request.post_id))
            print(response)
        except Exception as e:
            print(e)
        return dense_pb2.Response(message="OK")

    def predict_pipeline(self, request, context):
        post_id = request.postId
        folder_path = settings.FOLDER_PATH + post_id
        try:
            asyncio.run(download_unzip(self.gcs_client, folder_path, post_id))
            proxy = asyncio.run(task_manager(post_id))
            res = json.dumps(proxy, ensure_ascii=False).encode('utf-8')
            # TODO catch all err and return dense_pb2.Response(message="error message", error="error")
            return dense_pb2.Response(message=res, isNext=True)
        except Exception as e:
            print(e)


def print_thread(post_id):
    print("current_thread: {}, post: {}".format(
        current_thread().name, post_id))
    return


async def task_manager(post_id):
    t1 = asyncio.create_task(nsfw.http(post_id))
    t1.set_name("nsfw")
    t2 = asyncio.create_task(logo.http(post_id))
    t2.set_name("logo")
    tasks = [t1, t2]
    out = {}
    while tasks:
        finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for x in finished:
            result = x.result()
            # keep task counter, collect results and return when all tasks are finished
            if result:
                # check for result
                # cancel the other tasks, we have a result. We need to wait for the cancellations
                # to propagate.
                # for task in unfinished:
                #     await task.cancel()
                if x.get_name() == "nsfw":
                    key, val = get_max_from_list_of_dict(result)
                    if val > 0.5:
                        out[x.get_name()] = "True|{key}".format(key=key)
                    else:
                        out[x.get_name()] = "False"
                elif x.get_name() == "logo":
                    key, val = get_max_from_list_of_dict(result)
                    if val > 0.5:
                        out[x.get_name()] = "True|{key}".format(key=key)
                    else:
                        out[x.get_name()] = "False"
        tasks = unfinished
    return out

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
