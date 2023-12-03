import os
from flask import Flask, render_template, request
import cloudinary
from cloudinary.uploader import upload
import vars

app = Flask(__name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name=vars.CLOUDINARY_CLOUD_NAME,
    api_key=vars.CLOUDINARY_API_KEY,
    api_secret=vars.CLOUDINARY_API_SECRET,
)


def create_uploads_folder():
    # Create the "uploads" folder if it doesn't exist
    folder_path = "uploads"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def determine_resource_type(file_extension):
    # Define a basic mapping of file extensions to resource types
    image_extensions = {"jpg", "jpeg", "png", "gif", "bmp", "tiff"}
    video_extensions = {"mp4", "avi", "mov", "flv", "wmv"}

    if file_extension in image_extensions:
        return "image"
    elif file_extension in video_extensions:
        return "video"
    else:
        return None  # Unknown type or unsupported


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            create_uploads_folder()

            # Save the file locally
            file_path = f"uploads/{file.filename}"
            file.save(file_path)

            file_extension = os.path.splitext(file.filename)[1][1:].lower()
            resource_type = determine_resource_type(file_extension)

            if resource_type:
                # Upload the file to Cloudinary
                response = upload(
                    file_path,
                    resource_type=resource_type,
                    use_filename=True,
                    unique_filename=False,
                )

                if "url" in response:
                    # Delete the local file after upload (optional)
                    os.remove(file_path)

                    mime_type = file.mimetype
                    return render_upload_response(
                        resource_type, response["url"], mime_type
                    )
                else:
                    return "Upload failed."
            else:
                return "Unsupported file type."

    return render_template("index.html")


def render_upload_response(resource_type, url, mime_type):
    if resource_type == "video":
        return f"""
            <h1>Upload successful!</h1>
            <video controls>
                <source src="{url}" type="{mime_type}">
                Your browser does not support the video tag.
            </video>
            <p>URL: <a href="{url}">{url}</a></p>
            <p><a href="/">Upload another file</a></p>
        """
    elif resource_type == "image":
        return f"""
            <h1>Upload successful!</h1>
            <img src="{url}" alt="Uploaded image">
            <p>URL: <a href="{url}">{url}</a></p>
            <p><a href="/">Upload another file</a></p>
        """
    else:
        return "Error in rendering upload response."


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
