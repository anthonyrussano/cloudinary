import os
import sys

from image_upload.uploader import upload_file


def upload_to_cloudinary(file_path):
    try:
        response = upload_file(
            file_path,
            folder=os.environ.get("CLOUDINARY_FOLDER"),
        )
        print(f"Upload successful! URL: {response['secure_url'] or response['url']}")
    except Exception as exc:
        print(f"An error occurred: {exc}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    upload_to_cloudinary(file_path)
