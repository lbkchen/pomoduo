const express = require("express");
const app = express();
var path = require("path");
var http = require("http").Server(app);
var io = require("socket.io")(http);

app.use("/static", express.static(path.join(__dirname, "public")));

app.get("/", function(req, res) {
  res.sendFile(__dirname + "/index.html");
});

io.on("connection", function(socket) {
  console.log("a user connected");

  socket.on("start", function(msg) {
    console.log("start message received");
  });
});

http.listen(3000, function() {
  console.log("listening on *:3000");
});
