import os
import base64
import requests

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

MODEL_NAME = "@cf/black-forest-labs/flux-1-schnell"

CLOUDFLARE_URL = (
    f"https://api.cloudflare.com/client/v4/accounts/"
    f"{ACCOUNT_ID}/ai/run/{MODEL_NAME}"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def generate_image():
    if not ACCOUNT_ID or not API_TOKEN:
        return jsonify({
            "error": "Cloudflare credentials are not configured."
        }), 500

    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "").strip()

    try:
        number_of_images = int(data.get("number_of_images", 1))
    except (TypeError, ValueError):
        number_of_images = 1

    if not prompt:
        return jsonify({
            "error": "Please enter an image prompt."
        }), 400

    if len(prompt) > 2000:
        return jsonify({
            "error": "Prompt must be 2000 characters or fewer."
        }), 400

    number_of_images = max(1, min(number_of_images, 2))

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }

    images = []

    try:
        for _ in range(number_of_images):
            response = requests.post(
                CLOUDFLARE_URL,
                headers=headers,
                json={"prompt": prompt},
                timeout=120,
            )

            if not response.ok:
                app.logger.error(
                    "Cloudflare error %s: %s",
                    response.status_code,
                    response.text[:1000],
                )

                if response.status_code == 429:
                    return jsonify({
                        "error": (
                            "Cloudflare AI usage limit reached. "
                            "Please try again later."
                        )
                    }), 429

                return jsonify({
                    "error": (
                        "Cloudflare image generation failed. "
                        "Check your token, account ID, and Workers AI access."
                    )
                }), 502

            # Parse Cloudflare JSON response
            try:
                result = response.json()
            except ValueError:
                app.logger.error(
                    "Cloudflare returned non-JSON response: %s",
                    response.text[:1000],
                )
                return jsonify({
                    "error": "Cloudflare returned an unexpected response."
                }), 502

            # Extract base64 image from response
            image_base64 = result.get("result", {}).get("image")

            if not image_base64:
                app.logger.error(
                    "Cloudflare response did not contain image data: %s",
                    str(result)[:1000],
                )
                return jsonify({
                    "error": "Cloudflare response did not contain image data."
                }), 502

            # Create data URL for frontend display
            image_data_url = (
                f"data:image/jpeg;base64,{image_base64}"
            )

            images.append(image_data_url)

        return jsonify({"images": images})

    except requests.Timeout:
        return jsonify({
            "error": "Image generation timed out. Please try again."
        }), 504

    except requests.RequestException:
        app.logger.exception("Cloudflare connection error")
        return jsonify({
            "error": "Could not connect to Cloudflare AI."
        }), 502

    except Exception:
        app.logger.exception("Unexpected image generation error")
        return jsonify({
            "error": "Something went wrong while generating the image."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)