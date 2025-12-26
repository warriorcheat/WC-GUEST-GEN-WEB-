from flask import Flask, request, render_template
import requests
import json
import os

app = Flask(__name__)

API_URL = os.getenv("API_URL", "https://wc-guest-gen.vercel.app/gen")
TG_REGIONS = ["ME","IND","ID","VN","TH","BD","PK","TW","EU","RU","NA","SAC","BR"]

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", response=None, regions=TG_REGIONS)

@app.route("/gen", methods=["GET"])
def generate_accounts():
    name = request.args.get("name", "HUSTLER")
    count = request.args.get("count", "1")
    region = request.args.get("region", "IND").upper()

    try:
        count = int(count)
        if count < 1: count = 1
        if count > 15: count = 15
    except:
        count = 1
    if region not in TG_REGIONS:
        region = "IND"

    try:
        r = requests.get(API_URL, params={"name": name, "count": count, "region": region}, timeout=60)
        r.raise_for_status()
        data = r.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
    except Exception as e:
        pretty = f"⚠️ API Error: {e}"

    return render_template("index.html", response=pretty, regions=TG_REGIONS)

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=False)
