import settings

# create singleton
def download_unzip(download_path, gcs_object_path):
    try:
        from google.cloud import storage
        import tarfile
        import tempfile

        with tempfile.NamedTemporaryFile() as temp:
            temp.write(bytes(settings.CRED_JSON, 'utf-8'))
            temp.flush()
            storage_client = storage.Client.from_service_account_json(
                temp.name)

        bucket_name = settings.BUCKET_NAME
        object_path = gcs_object_path+"/raw/1.tar.gz" # need to update the gcs object path (refer from input url)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(object_path)

        localpath = settings.FOLDER_PATH + "1.tar.gz" # update accordingly as per line 17
        blob.download_to_filename(localpath)

        # unzip process
        tar = tarfile.open(localpath, "r:gz")
        tar.extractall(path=download_path)
        tar.close()
    except Exception as e:
        print(e)

def get_max_from_list_of_dict(list_of_dict):
    if len(list_of_dict) < 1:
        return
    filter_dict = {}
    for d in list_of_dict:
        v = list(d.values())
        max_v = max(v)
        k = list(d.keys())
        filter_dict[k[v.index(max_v)]] = max_v
    vals = list(filter_dict.values())
    keys = list(filter_dict.keys())
    return keys[vals.index(max(vals))], max(vals)

