const express = require("express");
const { Readable } = require("stream");

const app = express();

// Mengirimkan file HTML sederhana sebagai klien
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

// Endpoint untuk streaming data melalui SSE
app.get("/stream", (req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.flushHeaders();

  // Fungsi untuk mengirimkan data setiap detik
  const sendData = () => {
    const data = {
      message: "Pesan terkirim!",
      timestamp: new Date().toLocaleTimeString(),
    };
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  };

  // Mengirimkan data setiap detik
  const intervalId = setInterval(sendData, 1000);

  // Menutup koneksi SSE saat klien memutuskan
  req.on("close", () => {
    clearInterval(intervalId);
    res.end();
  });
});

// Menjalankan server pada port 3000
app.listen(3000, () => {
  console.log("Server berjalan di http://localhost:3000");
});
