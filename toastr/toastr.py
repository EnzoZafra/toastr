import vision.image_capture as ic
import upload_download.upload_image as upload
import upload_download.download_text as download
import os
import sys

IMAGE_DIR = "images/"
TOASTR_BUCKET = "toastr_image"

if __name__ == "__main__":
    # Execute script from script dir
    if os.path.dirname(sys.argv[0]) != '':
        os.chdir(os.path.dirname(sys.argv[0]))

    if not os.path.exists("./upload_download/processed_text"):
        os.makedirs("./upload_download/processed_text")

    if (ic.capture() == 0):
        most_recent_img = max([os.path.join(IMAGE_DIR, basename) for basename in os.listdir(IMAGE_DIR)], key=os.path.getctime)
        upload.upload_file(most_recent_img, TOASTR_BUCKET)
        os.chdir(os.path.dirname(sys.argv[0])+"upload_download")
        download.download_text()