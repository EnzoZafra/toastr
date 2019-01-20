import os
import time

from google.cloud import storage

def download_text():
    os.system("gsutil -m cp -R gs://toastr_processedtext/* ./processed_text")

def download_object(bucket_name, source_object_name, dest_filename, auth_file):
    timeout = 5

    storage_client = storage.Client.from_service_account_json(auth_file)
    bucket = storage_client.get_bucket(bucket_name)
    object_found = False
    start = time.time()

    while not object_found:
        elapsed = time.time() - start
        if elapsed > timeout:
            print("Processed text downloader timed out. " + source_object_name + " not found in " + bucket_name)
            break

        objects = bucket.list_blobs()
        for object in objects:
            print(object.name)
            if object.name == source_object_name:
                object_found = True
                blob = bucket.blob(source_object_name)
                blob.download_to_filename(dest_filename)

                print('Object {} downloaded to {}.'.format(
                    source_object_name,
                    dest_filename))
                break

if __name__ == "__main__":
    # download_text()
    download_object("toastr_processedtext", "bstwhiteboard.JPG.txt", "bstwhiteboard.txt", "auth.json")