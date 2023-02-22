// Get the host of the server
const host = window.location.host;

// Create a new WebSocket connection to the server
const websocket = new WebSocket("ws://" + host + "/web");

// When the connection is opened, change the background color of the body
websocket.onopen = function (event) {
	document.body.style.backgroundColor = "lightgreen";
};

// When a message is received, change the background color of the body depending on the message
websocket.onmessage = function (event) {
	if (event.data === "led on") {
		document.body.style.backgroundColor = "green";
	} else if (event.data === "led off") {
		document.body.style.backgroundColor = "red";
	}
};

document.getElementById("led-toggle").onclick = function () {
	if (document.body.style.backgroundColor == "red") {
		websocket.send("led on");
	} else {
		websocket.send("led off");
	}
};
