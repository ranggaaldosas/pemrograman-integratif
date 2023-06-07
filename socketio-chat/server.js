const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const path = require("path");

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Menambahkan baris ini untuk melayani file static dari direktori saat ini
app.use(express.static(path.join(__dirname)));

io.on("connection", (socket) => {
  console.log("User terkoneksi");

  socket.on("chat message", (msg) => {
    io.emit("chat message", msg);
  });

  socket.on("disconnect", () => {
    console.log("User disconnected");
  });
});

server.listen(3000, () => {
  console.log("Server telah berjalan pada port 3000");
});
