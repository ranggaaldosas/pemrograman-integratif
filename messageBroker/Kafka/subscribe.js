const { Kafka } = require('kafkajs');

async function run() {
  const kafka = new Kafka({
    clientId: 'my-app',
    brokers: ['localhost:9092'] // Ganti dengan alamat dan port broker Kafka Anda
  });

  const consumer = kafka.consumer({ groupId: 'test-group' });

  await consumer.connect();
  await consumer.subscribe({ topic: 'test-rangga', fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      console.log({
        key: message.key.toString(),
        value: message.value.toString(),
        headers: message.headers,
      });
    },
  });
}

run().catch(console.error);
