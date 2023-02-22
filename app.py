from flask import Flask, send_from_directory
from flask_sock import Sock as WebSocket, Server as WebSocketServer
from flask_cors import CORS

# Create a new flask server.
app = Flask(__name__)
CORS(app)
# Create a new websocket server.
websocket = WebSocket(app)
static_folder = app.static_folder = "static"

espWS: WebSocketServer | None = None
webWS: WebSocketServer | None = None

ledOn = False

def turn_on_led():
    if espWS is not None:
        espWS.send("led on")

def turn_off_led():
    if espWS is not None:
        espWS.send("led off")

def led_is_on():
    global ledOn
    if webWS is not None:
        webWS.send("led on")
        ledOn = True

def led_is_off():
    global ledOn
    if webWS is not None:
        webWS.send("led off")
        ledOn = False

# Create a new route for the websocket.
@websocket.route("/esp8266")
def on_connect_esp8266_route(ws: WebSocketServer):
    """
    This function is called when a new websocket connection is made.
    """
    global espWS, ledOn
    espWS = ws
    while True:
        message = ws.receive()
        if message == "button pressed":
            if ledOn:
                turn_off_led()
            else:
                turn_on_led()
        elif message == "LED on":
            led_is_on()
        elif message == "LED off":
            led_is_off()

@websocket.route("/web")
def on_connect_web_route(ws: WebSocketServer):
    """
    This function is called when a new websocket connection is made.
    """
    global webWS
    webWS = ws
    if ledOn:
        led_is_on()
    else:
        led_is_off()
    while True:
        message = ws.receive()
        if message == "led on":
            turn_on_led()
        elif message == "led off":
            turn_off_led()

@app.route("/<path:path>")
def path(path: str):
    return send_from_directory(static_folder, path)

@app.route("/")
def index():
    return send_from_directory(static_folder, "index.html")

def create_app():
    app.run(host="0.0.0.0", port=80)


if __name__ == "__main__":
    create_app()