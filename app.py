import os
from flask import Flask, render_template, request
import cloudinary
from cloudinary.uploader import upload

app = Flask(__name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)


def create_uploads_folder():
    # Create the "uploads" folder if it doesn't exist
    folder_path = "uploads"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            create_uploads_folder()

            # Save the file locally
            file_path = f"uploads/{file.filename}"
            file.save(file_path)

            # Upload the file to Cloudinary
            response = upload(file_path)

            if "url" in response:
                # Delete the local file after upload (optional)
                os.remove(file_path)

                return f"""
                    <h1>Upload successful!</h1>
                    <img src="{response['url']}" alt="Uploaded Image">
                    <p>URL: <a href="{response['url']}">{response['url']}</a></p>
                    <p><a href="/">Upload another image</a></p>
                """
            else:
                return "Upload failed."

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
