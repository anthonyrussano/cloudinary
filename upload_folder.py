from dotenv import load_dotenv

load_dotenv()
import os
import sys
import pathlib
import cloudinary

cloudinary.config(
cloud_name = "alchemist-cookbook",
api_key = "932566579288573",
api_secret = "yowIQbSIBvGgerz8sjG1NLgF8NI"
)

import cloudinary.uploader
import cloudinary.api

config = cloudinary.config(secure=True)
supported_files = (".png", ".jpg", ".jpeg", ".heic")

def upload_and_tag_image(filename, folder="uploads"):
    stem = pathlib.Path(filename).stem
    res = cloudinary.uploader.upload(
        filename,
        public_id=stem,
        folder=folder
    )
    return res

def upload_folder():
    n = 0
    for file in sorted(os.listdir("photos")):
        if pathlib.Path(file).suffix.lower() in supported_files:
            try:
                print('<img src="https://res.cloudinary.com/alchemist-cookbook/image/upload/f_auto/uploads/' + file + '" style="border-radius: 25px;border-width: 2px;border-style:inset;width: 600px;">')
                upload_and_tag_image("photos/" + file)
                os.remove("photos/" + file)
                n += 1
            except Exception as e:
                print("failed for ", file)
                print(e)
    print(n, " photos uploaded")

upload_folder()