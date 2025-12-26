from flask import Flask, request, Markup
import requests
import json
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = Flask(__name__)

# API base URL
API_URL = os.getenv("API_URL", "https://wc-guest-gen.vercel.app/")
TG_REGIONS = ["ME","IND","ID","VN","TH","BD","PK","TW","EU","RU","NA","SAC","BR"]

def render_page(response=None):
    """Return full HTML page with optional response"""
    regions_options = "".join([f'<option value="{r}">{r}</option>' for r in TG_REGIONS])
    response_block = f"<pre>{response}</pre>" if response else ""
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WC PREMIUM GUEST ID GENERATOR</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ margin:0; font-family:'Roboto', sans-serif; background:#0f0f0f; color:#fff; overflow-x:hidden; }}
        #particles-js {{ position:fixed; width:100%; height:100%; z-index:-1; top:0; left:0; }}
        .container {{ max-width:700px; margin:50px auto; padding:30px; background:rgba(20,20,20,0.85); border-radius:15px; box-shadow:0 0 30px rgba(0,255,255,0.3); }}
        h1 {{ text-align:center; color:#00ffff; }}
        form input, form select {{ width:100%; padding:12px; margin:10px 0; border-radius:10px; border:none; outline:none; font-size:16px; }}
        input[type="submit"] {{ background:#00ffff; color:#000; font-weight:bold; cursor:pointer; transition:0.3s; }}
        input[type="submit"]:hover {{ background:#0ff; transform:scale(1.05); }}
        pre {{ background:#111; padding:15px; border-radius:10px; overflow-x:auto; margin-top:20px; color:#0ff; white-space:pre-wrap; word-wrap:break-word; }}
    </style>
    </head>
    <body>

    <div id="particles-js"></div>

    <div class="container">
        <h1>🚀 WC PREMIUM GUEST ID GENERATOR</h1>
        <form method="get" action="/gen">
            <label>Region</label>
            <select name="region">{regions_options}</select>
            <label>Name Prefix</label>
            <input type="text" name="name" placeholder="ID NAME">
            <label>Account Count (1-15)</label>
            <input type="number" name="count" value="1" min="1" max="15">
            <input type="submit" value="Generate Guest ID">
        </form>
        {response_block}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
    <script>
    particlesJS("particles-js", {{
      "particles": {{
        "number": {{ "value": 80 }},
        "color": {{ "value": "#0ff" }},
        "shape": {{ "type": "circle" }},
        "opacity": {{ "value": 0.5 }},
        "size": {{ "value": 3 }},
        "line_linked": {{ "enable": true, "distance": 150, "color": "#0ff", "opacity": 0.4, "width": 1 }},
        "move": {{ "enable": true, "speed": 2 }}
      }},
      "interactivity": {{
        "events": {{
          "onhover": {{ "enable": true, "mode": "repulse" }},
          "onclick": {{ "enable": true, "mode": "push" }}
        }},
        "modes": {{ "repulse": {{ "distance": 100 }} }}
      }},
      "retina_detect": true
    }});
    </script>

    </body>
    </html>
    """
    return html

@app.route("/", methods=["GET"])
def home():
    return render_page()

@app.route("/gen", methods=["GET"])
def generate_accounts():
    name = request.args.get("name", "HUSTLER")
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

    # Call API
    try:
        r = requests.get(
            API_URL + "gen",
            params={"name": name, "count": count, "region": region},
            timeout=30
        )
        r.raise_for_status()
        data = r.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
    except requests.exceptions.RequestException as e:
        pretty = f"⚠️ API Request Error: {e}"
    except json.JSONDecodeError:
        pretty = "⚠️ API Response is not valid JSON."

    return render_page(response=Markup(pretty))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
