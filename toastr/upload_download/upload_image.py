import subprocess


def upload_file(image_path, bucket_name):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    subprocess.run(["gsutil", "cp", image_path, f"gs://{bucket_name}"])
