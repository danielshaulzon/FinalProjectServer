from flask import Flask
from flask_sock import Sock as WebSocket, Server as WebSocketServer

# Create a new flask server.
server = Flask(__name__)
# Create a new websocket server.
websocket = WebSocket(server)

# Create a new route for the websocket.
@websocket.route("/esp8266")
def on_connect_esp8266_route(ws: WebSocketServer):
    """
    This function is called when a new websocket connection is made.
    """
    while True:
        message = ws.receive()
        if message == "button pressed":
            ws.send("led on")
        elif message == "button released":
            ws.send("led off")

if __name__ == "__main__":
    server.run(port=3000, host="0.0.0.0")
