from flask import Flask, request, Markup
import requests
import json
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)

API_URL = os.getenv("API_URL", "https://wc-guest-gen.vercel.app/")
TG_REGIONS = ["ME","IND","ID","VN","TH","BD","PK","TW","EU","RU","NA","SAC","BR"]

def render_page(response=None):
    regions_options = "".join([f'<option value="{r}">{r}</option>' for r in TG_REGIONS])
    response_block = f"<pre>{response}</pre>" if response else ""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WC PREMIUM GUEST ID GENERATOR</title>
    <style>
        body {{ background:#0f0f0f; color:#0ff; font-family:sans-serif; }}
        .container {{ max-width:700px; margin:50px auto; padding:30px; background:rgba(20,20,20,0.85); border-radius:15px; }}
        input, select {{ width:100%; padding:10px; margin:5px 0; border-radius:5px; }}
        input[type=submit] {{ cursor:pointer; font-weight:bold; }}
        pre {{ background:#111; padding:10px; border-radius:5px; overflow-x:auto; }}
    </style>
    </head>
    <body>
    <div class="container">
        <h1>🚀 WC PREMIUM GUEST ID GENERATOR</h1>
        <form method="get" action="/gen">
            <label>Region</label>
            <select name="region">{regions_options}</select>
            <label>Account Count (1-15)</label>
            <input type="number" name="count" value="1" min="1" max="15">
            <input type="submit" value="Generate Guest ID">
        </form>
        {response_block}
    </div>
    </body>
    </html>
    """

def call_api(region, count, retries=2, timeout=5):
    params = {"region": region, "count": count}
    for attempt in range(retries + 1):
        try:
            response = requests.get(API_URL + "gen", params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            if attempt < retries:
                time.sleep(0.5)  # wait half second before retry
                continue
            else:
                raise

@app.route("/", methods=["GET"])
def home():
    return render_page()

@app.route("/gen", methods=["GET"])
def generate_accounts():
    count = request.args.get("count", "1")
    region = request.args.get("region", "IND").upper()

    # Validate count
    try:
        count = int(count)
        if count < 1: count = 1
        if count > 15: count = 15
    except ValueError:
        count = 1

    if region not in TG_REGIONS:
        region = "IND"

    try:
        data = call_api(region, count)
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
    except Exception as e:
        pretty = f"⚠️ API Request Error: {e}"

    return render_page(response=Markup(pretty))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
