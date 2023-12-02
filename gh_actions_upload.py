import os
import sys
from cloudinary.uploader import upload

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)

def upload_to_cloudinary(file_path):
    """
    Uploads a file to Cloudinary and prints the URL of the uploaded file.
    :param file_path: Path to the file to be uploaded.
    """
    try:
        response = upload(file_path)
        if "url" in response:
            print(f"Upload successful! URL: {response['url']}")
        else:
            print("Upload failed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    upload_to_cloudinary(file_path)
