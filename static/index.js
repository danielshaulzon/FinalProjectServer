// Get the host of the server
const host = window.location.host;

// Create a new WebSocket connection to the server
const websocket = new WebSocket("ws://" + host + "/web");

const redLedDiv = document.getElementById("red-led-div");
const greenLedDiv = document.getElementById("green-led-div");
const redLedBtn = document.getElementById("red-led-toggle");
const greenLedBtn = document.getElementById("green-led-toggle");

// When the connection is opened, change the background color of the body
websocket.onopen = function (event) {
	redLedDiv.style.backgroundColor = "lightcoral";
	greenLedDiv.style.backgroundColor = "lightgreen";
	setTimeout(function() {
		const password = prompt("Enter password");
		if (password) {
			websocket.send(`password ${password}`);
		}
	}, 200);
};

// When a message is received, change the background color of the body depending on the message
websocket.onmessage = function (event) {
	console.log(event.data);
	if (event.data == "password valid") {
		redLedBtn.disabled = false;
		greenLedBtn.disabled = false;
	}
	if (event.data === "red led is on") {
		redLedDiv.style.backgroundColor = "red";
	} else if (event.data === "red led is off") {
		redLedDiv.style.backgroundColor = "lightcoral";
	} else if (event.data === "green led is on") {
		greenLedDiv.style.backgroundColor = "green";
	} else if (event.data === "green led is off") {
		greenLedDiv.style.backgroundColor = "lightgreen";
	}
};

redLedBtn.onclick = function () {
	websocket.send("red led toggle");
};

greenLedBtn.onclick = function () {
	websocket.send("green led toggle");
};