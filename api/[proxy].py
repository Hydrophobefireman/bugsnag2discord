# Ported from https://github.com/marcopolee/hookbot/blob/master/index.js

import requests
from flask import Flask, request


app = Flask(__name__)


@app.route("/", methods=["get", "post"])
@app.route("/api/", methods=["get", "post"])
def catch_all():
    return "ok"


@app.route("/send", strict_slashes=False, methods=["post"])
def send():
    discord_url = request.args["discord_url"]
    bug = request.json

    error_title = f"{bug['error']['exceptionClass']}: {bug['error']['message']}"
    method = bug["error"]["context"]
    app = bug["project"]["name"]
    environment = bug["error"]["releaseStage"]
    error_url = bug["error"]["url"]
    fields = [
        {
            "name": "Error",
            "value": error_title,
        }
    ]
    if bug.get("stackTrace"):
        loc = f"{bug['stackTrace']['file']}:${bug['stackTrace']['lineNumber']} - ${bug['stackTrace']['method']}"
        fields.append({"name": "Location", "value": loc})

    message = {
        "embeds": [
            {
                "title": f"Event in {environment} from {app} in {method}",
                "url": error_url,
                "fields": fields,
            }
        ]
    }
    requests.post(discord_url, json=message)
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
