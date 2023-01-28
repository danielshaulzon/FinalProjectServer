from flask import Flask, send_from_directory
from flask_sock import Sock as WebSocket, Server as WebSocketServer

# Create a new flask server.
app = Flask(__name__)
# Create a new websocket server.
websocket = WebSocket(app)
static_folder = app.static_folder = "static"

espWS: WebSocketServer | None = None
webWS: WebSocketServer | None = None

def turn_on_led():
    if espWS is not None:
        espWS.send("led on")

def turn_off_led():
    if espWS is not None:
        espWS.send("led off")

def led_is_on():
    if webWS is not None:
        webWS.send("led on")

def led_is_off():
    if webWS is not None:
        webWS.send("led off")

# Create a new route for the websocket.
@websocket.route("/esp8266")
def on_connect_esp8266_route(ws: WebSocketServer):
    """
    This function is called when a new websocket connection is made.
    """
    global espWS
    espWS = ws
    while True:
        message = ws.receive()
        if message == "LED on":
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

if __name__ == "__main__":
    app.run()
