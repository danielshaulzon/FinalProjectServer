from flask import Flask, send_from_directory
from flask_sock import Sock as WebSocket, Server as WebSocketServer
from flask_cors import CORS
from typing import Union

# Create a new flask server.
app = Flask(__name__)
CORS(app)
# Create a new websocket server.
websocket = WebSocket(app)
app.static_folder = "static"

espWS = None
webWS = None

redLedOn = False
greenLedOn = False

def turn_on_led(led: str):
    if espWS is not None:
        espWS.send(f"{led} led on")

def turn_off_led(led: str):
    if espWS is not None:
        espWS.send(f"{led} led off")

def toggle_led(led: str):
     if espWS is not None:
        espWS.send(f"{led} led toggle")

def notify_web(led: str, state: str):
    if webWS is not None:
        webWS.send(f"{led} led is {state}")

# Create a new route for the websocket.
@websocket.route("/esp8266")
def on_connect_esp8266_route(ws: WebSocketServer):
    """
    This function is called when a new websocket connection is made.
    """
    global espWS, redLedOn, greenLedOn
    espWS = ws
    while True:
        message: str = ws.receive()
        split = message.split()
        # button pressed
        if len(split) == 3 and split[1] == "button" and split[2] == "pressed":
            led = split[0]
            toggle_led(led)
        # color changed
        elif len(split) == 4 and split[1] == "led" and split[2] == "turned":
            led, state = split[0], split[3]
            notify_web(led, state)
            if led == "red":
                if state == "on":
                    redLedOn = True
                else:
                    redLedOn = False
            elif led == "green":
                if state == "on":
                    greenLedOn = True
                else:
                    greenLedOn = False

@websocket.route("/web")
def on_connect_web_route(ws: WebSocketServer):
    """
    This function is called when a new websocket connection is made.
    """
    global webWS
    webWS = ws
    if redLedOn:
        notify_web("red", "on")
    else:
        notify_web("red", "off")
    if greenLedOn:
        notify_web("green", "on")
    else:
        notify_web("green", "off")
    while True:
        message: str = ws.receive()
        split = message.split()
        if len(split) == 2 and split[0] == "password" and split[1] == "daniel":
            ws.send("password valid")
        if len(split) == 3 and split[1] == "led" and split[2] == "toggle":
            led = split[0]
            toggle_led(led)

@app.route("/<path:path>")
def path(path: str):
    return send_from_directory(app.static_folder, path)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

def create_app():
    app.run(host="0.0.0.0", port=3000)


if __name__ == "__main__":
    create_app()