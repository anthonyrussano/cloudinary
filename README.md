# image-upload

Small CLI tool for agent-friendly Cloudinary image operations. All commands return JSON.

## What It Does

- Upload local files to Cloudinary
- Check whether an asset already exists by `public_id`
- Search images by `public_id` prefix or Cloudinary tag
- Download either the transformed site image or the original uploaded asset

## Setup

The CLI reads credentials from a local `.env` file automatically, or from exported shell variables.

Required variables:

```bash
export CLOUDINARY_CLOUD_NAME=your_cloud_name
export CLOUDINARY_API_KEY=your_api_key
export CLOUDINARY_API_SECRET=your_api_secret
```

Install dependencies:

```bash
uv sync
```

## Usage

Upload a file:

```bash
uv run image-upload /path/to/photo.jpg
```

Upload with a fixed `public_id` and validate the site-style transformed URL:

```bash
uv run image-upload /path/to/photo.jpg --public-id lemon --validate-url
```

Upload into a folder:

```bash
uv run image-upload /path/to/photo.jpg --folder agent-uploads --public-id my-photo
```

Check whether a `public_id` already exists:

```bash
uv run image-upload --check-only --public-id lemon
```

Search by `public_id` prefix:

```bash
uv run image-upload --search-prefix lem --max-results 5
```

Search by tag:

```bash
uv run image-upload --search-tag citrus --max-results 5
```

Download the transformed site image:

```bash
uv run image-upload --download --public-id lemon --output-dir /tmp/cloudinary-images
```

Download the original uploaded asset:

```bash
uv run image-upload --download --download-original --public-id lemon --output-dir /tmp/cloudinary-images-original
```

Compatibility entrypoint:

```bash
uv run app.py /path/to/photo.jpg
```

Notes:

- `--search-prefix` and `--search-tag` are mutually exclusive.
- The default image delivery URL format is `https://res.cloudinary.com/<cloud_name>/image/upload/w_200,f_auto/<public_id>`.
- `--resource-type` defaults to `image`.

Example upload result:

```json
{
  "ok": true,
  "result": {
    "local_path": "/path/to/photo.jpg",
    "exists_before_upload": false,
    "public_id": "lemon",
    "resource_type": "image",
    "secure_url": "https://res.cloudinary.com/...",
    "url": "http://res.cloudinary.com/...",
    "delivery_url": "https://res.cloudinary.com/alchemist-cookbook/image/upload/w_200,f_auto/lemon",
    "delivery_url_valid": true
  }
}
```

Example existence check result:

```json
{
  "ok": true,
  "result": {
    "public_id": "lemon",
    "exists": true,
    "delivery_url": "https://res.cloudinary.com/alchemist-cookbook/image/upload/w_200,f_auto/lemon"
  }
}
```

Example download result:

```json
{
  "ok": true,
  "result": {
    "public_id": "Lemon",
    "resource_type": "image",
    "download_type": "original",
    "source_url": "https://res.cloudinary.com/alchemist-cookbook/image/upload/v1539395623/Lemon.jpg",
    "local_path": "/tmp/cloudinary-images-original/Lemon.jpg",
    "bytes": 309688
  }
}
```
