from flask import Flask, render_template_string, request
from mcrcon import MCRcon
import re

# Minecraft server info
HOST = "those-communications.gl.at.ply.gg"
PORT = 12121
PASSWORD = "admin"

# Flask app
app = Flask(__name__)

# HTML template with responsive CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minecraft RCON Console</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1e1e1e;
            color: #fff;
            text-align: center;
            padding: 20px;
            margin: 0;
        }
        h1 { color: #4CAF50; font-size: 2em; margin-bottom: 20px; }
        form { display: flex; flex-direction: column; align-items: center; }
        input[type=text] {
            width: 90%;
            max-width: 500px;
            padding: 12px;
            margin: 10px 0;
            border-radius: 5px;
            border: none;
            font-size: 1em;
        }
        input[type=submit] {
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            background-color: #4CAF50;
            color: #fff;
            font-size: 1em;
            cursor: pointer;
        }
        input[type=submit]:hover { background-color: #45a049; }
        .response {
            margin-top: 20px;
            background-color: #333;
            padding: 15px;
            border-radius: 5px;
            text-align: left;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-width: 90%;
            max-height: 400px;
            overflow-y: auto;
            margin-left: auto;
            margin-right: auto;
        }
        @media (max-width: 600px) {
            h1 { font-size: 1.5em; }
            input[type=text], input[type=submit] { font-size: 0.9em; padding: 10px; }
            .response { max-height: 300px; padding: 10px; }
        }
    </style>
</head>
<body>
    <h1>Minecraft RCON Console</h1>
    <form method="POST">
        <input type="text" name="command" placeholder="Enter command" required>
        <input type="submit" value="Send">
    </form>
    {% if response %}
        <div class="response">
            <strong>Server Response:</strong>
            <pre>{{ response }}</pre>
        </div>
    {% endif %}
</body>
</html>
"""

# Helper function to strip Minecraft color codes
def strip_minecraft_colors(text):
    return re.sub(r"§.", "", text)

@app.route("/", methods=["GET", "POST"])
def console():
    response = ""
    if request.method == "POST":
        command = request.form.get("command")
        try:
            with MCRcon(HOST, PASSWORD, port=PORT) as mcr:
                raw_resp = mcr.command(command)
                response = strip_minecraft_colors(raw_resp)
        except Exception as e:
            response = f"Error: {e}"
    return render_template_string(HTML_TEMPLATE, response=response)

if __name__ == "__main__":
    print("Starting Minecraft RCON web console on http://localhost:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=False)
