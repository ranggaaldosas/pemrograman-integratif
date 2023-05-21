const mqtt = require('mqtt');

// Konfigurasi
const brokerUrl = 'mqtt://broker.hivemq.com'; // Ubah URL broker sesuai kebutuhan Anda
const topic = 'pesan-rangga'; // Ubah topik sesuai kebutuhan Anda

// Membuat klien MQTT
const client = mqtt.connect(brokerUrl);

// Menghubungkan klien ke broker
client.on('connect', () => {
  console.log('Klien terhubung ke broker HiveMQ');

  // Mengirim pesan ke topik tertentu
  const message = 'Halo, ini pesan dari klien MQTT!';
  client.publish(topic, message, (err) => {
    if (err) {
      console.error('Gagal mengirim pesan:', err);
    } else {
      console.log('Pesan berhasil dikirim ke topik:', topic);
      client.end(); // Mengakhiri koneksi setelah mengirim pesan
    }
  });
});
