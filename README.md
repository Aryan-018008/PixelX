# PixelX — AI Image Generator

**Your Imagination. One Prompt Away.**

PixelX is a lightweight AI image-generation web app that turns text prompts into images. It uses a Flask backend, a simple HTML/CSS/JavaScript frontend, and Cloudflare Workers AI for image generation.

# Deployment
PixelX is live at - https://pixelx-18-7glc.onrender.com/

## Features

- Text-to-image generation from user prompts
- Generate up to 2 images per request
- Responsive, dark-themed interface
- Image previews and downloads
- Loading/progress UI and error messages
- Server-side API credentials (not exposed to the browser)

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Image generation:** Cloudflare Workers AI — FLUX.1 Schnell
- **Environment variables:** `python-dotenv`
- **HTTP requests:** `requests`
- **Deployment:** Render

## Project Structure

```text
PixelX/
├── app.py
├── .env                  # Local secrets (not committed)
├── .gitignore
├── requirements.txt
├── templates/
│   └── index.html
└── testing/
    └── installation_check.py
```

## Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd PixelX
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
```

Never commit `.env` or expose the token in frontend code.

### 5. Start the Flask server

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## API

### `POST /api/generate`

Request JSON:

```json
{
  "prompt": "A tiny cabin in a snowy forest at sunset",
  "number_of_images": 1
}
```

Successful response:

```json
{
  "images": [
    "data:image/jpeg;base64,..."
  ]
}
```

The endpoint validates the prompt and returns image data URLs for the frontend. The requested image count is capped at 2.

## Deploy on Render

1. Push the project to GitHub.
2. In Render, create a **Web Service** and connect the repository.
3. Build command:

   ```bash
   pip install -r requirements.txt
   ```

4. Start command:

   ```bash
   gunicorn app:app
   ```

5. Add these environment variables in Render's **Environment** settings:
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ACCOUNT_ID`

6. Ensure `gunicorn` is listed in `requirements.txt`. If it is missing, install it locally and update the file:

   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```

Do not upload `.env` to Render or GitHub; set secrets in Render's environment settings.

## Security Notes

- Keep Cloudflare credentials in environment variables.
- Keep `.env` listed in `.gitignore`.
- Never commit API tokens or paste them into public issue trackers.
- If a token is exposed, revoke it and create a replacement.

## Current Status

PixelX V1 includes the frontend, Flask endpoint, and Cloudflare Workers AI integration. Verify model access and account usage limits in Cloudflare before deploying or sharing publicly.

## Author

Aryan Bharadwaj
