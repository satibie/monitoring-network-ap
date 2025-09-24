from flask import Flask, jsonify, send_from_directory 
import subprocess
import re

app = Flask(__name__)

ACCESS_POINTS = {
    "192.168.70.17": "R. Pertemuan",
    "192.168.70.18": "R. Transit",
    "192.168.70.244": "Rawat Inap",
    "192.168.70.25": "IGD",
    "192.168.70.16": "Farmasi",
    "192.168.70.21": "Rawat Jalan Lt.2",
    "192.168.70.23": "Rawat Jalan Lt.3",
    "192.168.70.1": "Mikrotik",
}

def ping(ip):
    try:
        output = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout = output.stdout

        # cek TTL = online?
        if "TTL=" in stdout:
            # regex cari "time=XXms"
            match = re.search(r"time[=<]\s*(\d+)ms", stdout)
            latency = int(match.group(1)) if match else None
            return True, latency
        else:
            return False, None
    except Exception:
        return False, None

@app.route("/status")
def status():
    result = {}
    for ip, name in ACCESS_POINTS.items():
        ok, latency = ping(ip)
        result[ip] = {
            "name": name,
            "status": "Online" if ok else "Offline",
            "latency": latency
        }
    return jsonify(result)

@app.route("/")
def index():
    return send_from_directory(".", "templates/index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
