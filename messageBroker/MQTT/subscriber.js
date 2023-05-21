const mqtt = require('mqtt');

// Konfigurasi
const brokerUrl = 'mqtt://broker.hivemq.com'; // Ubah URL broker sesuai kebutuhan Anda
const topic = 'pesan-rangga'; // Ubah topik sesuai kebutuhan Anda

// Membuat klien MQTT
const client = mqtt.connect(brokerUrl);

// Menghubungkan klien ke broker
client.on('connect', () => {
  console.log('Klien terhubung ke broker HiveMQ');

  // Melakukan subscribe ke topik tertentu
  client.subscribe(topic, (err) => {
    if (err) {
      console.error('Gagal melakukan subscribe:', err);
    } else {
      console.log('Berhasil melakukan subscribe ke topik:', topic);
    }
  });
});

// Menerima pesan yang diterima
client.on('message', (topic, message) => {
  console.log('Menerima pesan dari topik:', topic);
  console.log('Isi Pesan:', message.toString());
});
