// let socket = io();
const socket = io({ transports: ["websocket"], origins: "*" });

socket.on("gesture", function(message) {
  console.warn(`Gesture received by JS client: ${message}`);
});

socket.on("info", function(message) {
  console.warn(`Info received by JS client: ${message}`);
  try {
    const info = JSON.parse(message);
    // const info = message;
    console.log(info);
    document.getElementById("time").textContent = `${info.elapsed}`;
  } catch (error) {
    console.error(`Bad JSON received: ${error}`);
  }
});

socket.on("message", function(message) {
  console.warn("Catch all this message was caught:", message);
});

async function startTimer() {
  socket.emit("start", "hello");
  console.log(socket.disconnected);
}
