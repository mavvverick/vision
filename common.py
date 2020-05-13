import settings
from google.cloud import storage, exceptions 
import tempfile
import os, zipfile, shutil

# create singleton
# ref -> https://medium.com/better-programming/singleton-in-python-5eaa66618e3d
class Singleton:

    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)

@Singleton
class GCSClient(object):

    def __init__(self):
        try:
            with tempfile.NamedTemporaryFile() as temp:
                temp.write(bytes(settings.CRED_JSON, 'utf-8'))
                temp.flush()
                self.storage_client = storage.Client.from_service_account_json(temp.name)
        except Exception as e:
            print(e)
    
    def __repr__(self):
        return self.storage_client.__repr__()

async def download_unzip(client, download_path, gcs_object_path):
    try:
        bucket_name = settings.BUCKET_NAME
        object_path = gcs_object_path +"/frames.zip"
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(object_path)

        localpath = settings.FOLDER_PATH + gcs_object_path + "-frames.zip"
        blob.download_to_filename(localpath)

        # unzip process
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        zf = zipfile.ZipFile(localpath)
        for name in zf.namelist():
            try:
                f_in = zf.open(name)
                fname = name.split("/")
                with open(download_path+"/"+fname[2], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            except:
                pass
    except exceptions.NotFound:
        raise exceptions.NotFound("no zip found")
    except Exception as e:
        raise e
    finally:
        if os.path.exists(localpath):
            os.remove(localpath)

# [{"a":1, "b":2},{"a":3, "b":2},{"a":5, "b":7}] --> will return highest key, value i.e (b, 7)
def get_max_from_list_of_dict(list_of_dict):
    if len(list_of_dict) < 1:
        return
    filter_dict = list_of_dict[0]
    for d in list_of_dict:
        d.pop('neutral', None)
        v = list(d.values())
        max_v = max(v)
        k = list(d.keys())
        if max_v > filter_dict[k[v.index(max_v)]]:
            filter_dict[k[v.index(max_v)]] = max_v
    vals = list(filter_dict.values())
    keys = list(filter_dict.keys())
    max_v = max(vals)
    return keys[vals.index(max_v)], max_v


