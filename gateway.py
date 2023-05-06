from flask import Flask, request, jsonify
from os import environ as env
from flask_cors import CORS
import requests
import random
import psutil
import yaml

gateway = Flask(__name__)

CORS(gateway, resources={r"/*": {"origins": "*"}})


def load_configuration(path):
    with open(path) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config


config = load_configuration("gateway.yaml")


@gateway.route("/")
def index():
    response = {
        "health": {},
        "services": [],
    }

    if bool(env.get("LOG_HEALTH", 0)):
        response["health"] = {
            "cpu": {
                "usage": f"{psutil.cpu_percent()}%",
            },
            "ram": {
                "total": f"{float(psutil.virtual_memory().total / 1024 / 1024).__round__(2)} MB",
                "available": f"{float(psutil.virtual_memory().available / 1024 / 1024).__round__(2)} MB",
            },
            "disk": {
                "total": f"{float(psutil.disk_usage('/').total / 1024 / 1024 / 1024).__round__(2)} GB",
                "available": f"{float(psutil.disk_usage('/').free / 1024 / 1024 / 1024).__round__(2)} GB"
            },
        }

    if bool(env.get("LOG_SERVICES", 0)):
        for entry in config["paths"]:
            response["services"].append(entry["path"])

    return jsonify(response), 200



@gateway.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELELTE', 'PATCH'])
@gateway.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELELTE', 'PATCH'])
def path_router(path):
    try:
        parts = request.full_path.split('/')
        pathsReq = '/'.join(parts[2:]).replace("?", "")
        service = parts[1].replace("?", "")
        
        for entry in config["paths"]:
            if ("/" + service) == entry["path"]:
                    response = requests.request(
                        method=request.method,
                        url=random.choice(entry["servers"]) + "/" + pathsReq,
                        headers={key: value for (key, value) in request.headers if key != "Host"},
                        data=request.get_data(),
                        cookies=request.cookies,
                        allow_redirects=False,
                        timeout=5,
                    )

                    return (
                        response.content,
                        response.status_code,
                        response.headers.items(),
                    )
                    
        return "Gateway Not Found Service", 418
    except requests.exceptions.ConnectionError:
        return "Service Unavailable", 503
    except requests.exceptions.Timeout:
        return "Service Timeout Service", 408
    except requests.exceptions.TooManyRedirects:
        return "Service Too Many Redirects", 421
    except Exception as e:
        print(e)
        return "Gateway Internal Server Error", 418

if __name__ == "__main__":
    gateway.run(host="0.0.0.0", port=env.get("GATEWAY_APP_LOCAL_PORT", 8804), debug=True)
