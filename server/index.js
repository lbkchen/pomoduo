var app = require("express")();
var http = require("http").Server(app);
var io = require("socket.io")(http);

app.get("/", function(req, res) {
  res.sendFile(__dirname + "/index.html");
});

io.on("connection", function(socket) {
  console.log("a user connected");
  io.emit("update", "Update from the server.");
  socket.on("message", function(msg) {
    console.log(`Message received ${msg}`);
    io.emit("Sent a broadcasted message.");
  });
});

http.listen(3000, function() {
  console.log("listening on *:3000");
});
