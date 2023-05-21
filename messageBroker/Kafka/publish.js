const { Kafka } = require('kafkajs');

async function run() {
  const kafka = new Kafka({
    clientId: 'my-app',
    brokers: ['localhost:2181'] // Ganti dengan alamat dan port broker Kafka Anda
  });

  const producer = kafka.producer();

  await producer.connect();

  const message = {
    key: 'my-key',
    value: 'Hello, Kafka!'
  };

  await producer.send({
    topic: 'test-rangga',
    messages: [message]
  });

  await producer.disconnect();
}

run().catch(console.error);
