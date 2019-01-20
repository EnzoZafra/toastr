import os

def download_text():
    os.system("gsutil -m cp -R gs://toastr_processedtext/* ./processed_text")

if __name__ == "__main__":
    download_text()

